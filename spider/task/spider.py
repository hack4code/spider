# -*- coding: utf-8 -*-


import re
import requests

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import redis

from celery.utils.log import get_task_logger
from celery import Celery

from lxml import etree
from lxml.etree import QName

from scrapy.utils.project import get_project_settings


from mydm.model import save_spider_settings, save_feed, is_exists_spider
from mydm.spiderfactory import mk_spider_cls
from mydm.util import parse_redis_url

settings = get_project_settings()
app = Celery('tasks', broker=settings['BROKER_URL'])
app.conf.CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
app.conf.CELERYD_MAX_TASKS_PER_CHILD = 1


def get_feed_name(url):
    parser = urlparse(url)
    names = parser.hostname.split('.')
    if len(names) == 1:
        return re.sub(r'[^a-zA-Z]',
                      '',
                      names[0]
                      ).capitalize()
    else:
        return ''.join([re.sub(r'[^a-z]',
                               '',
                               name.lower()
                               ).capitalize()
                        for name in names[:-1]
                        if name.lower() != 'www'])


def check_spider(setting_):
    import uuid
    from scrapy.crawler import CrawlerProcess

    setting = setting_.copy()
    spid = str(uuid.uuid4())
    setting['_id'] = spid
    cls = mk_spider_cls(setting)
    custom_settings = {'ITEM_PIPELINES': {'mydm.pipelines.StatsPipeline':
                                          255},
                       'WEBSERVICE_ENABLED': False,
                       'TELNETCONSOLE_ENABLED': False,
                       'LOG_LEVEL': 'INFO',
                       'LOG_STDOUT': True,
                       'LOG_ENABLED': True,
                       'SPIDER_STATS_URL': settings['TEMP_SPIDER_STATS_URL']}

    p = CrawlerProcess(custom_settings)
    p.crawl(cls)
    p.start()

    def get_stats(custom_settings):
        conf = parse_redis_url(custom_settings['SPIDER_STATS_URL'])
        r = redis.Redis(host=conf.host,
                        port=conf.port,
                        db=conf.database)
        n = r.get(spid)
        r.delete(spid)
        return 0 if n is None else int(n)

    n = get_stats(custom_settings)
    return True if n > 0 else False


def _gen_lxmlspider(url, args):
    logger = get_task_logger(settings['LOGGER_NAME'])
    r = requests.get(url,
                     headers=settings['DEFAULT_REQUEST_HEADERS'])
    if r.status_code != 200:
        logger.error((
            'download {} error: status={}'
            ).format(url,
                     r.status_code))
        return False
    parser = etree.XMLParser(ns_clean=True)
    root = etree.XML(r.content,
                     parser)
    while len(root) == 1:
        root = root[0]
    setting = {'start_urls': [url]}
    for e in root:
        try:
            en = QName(e.tag).localname.lower()
        except ValueError:
            continue
        if en == 'title':
            setting['title'] = re.sub(r'^(\r|\n|\s)+|(\r|\n|\s)+$',
                                      '',
                                      e.text)
    setting['name'] = get_feed_name(url)
    if 'title' not in setting:
        setting['title'] = setting['name']
    setting['category'] = args['category']
    if setting['category'] not in settings['ARTICLE_CATEGORIES']:
        logger.error(u'{} category error'.format(setting['category']))
        return False
    attrs = ('item_content_xpath', 'removed_xpath_nodes')
    setting.update({k: args[k] for k in attrs if k in args})
    setting['type'] = 'xml'
    if check_spider(setting):
        save_spider_settings(setting)
        return True
    logger.error('gen_lxmlspider error for {}'.format(url))
    return False


@app.task(name='lxmlspider-creator')
def gen_lxmlspider(args):
    logger = get_task_logger(settings['LOGGER_NAME'])
    url = args['url']
    logger.info('gen_lxmlspider for {}'.format(url))
    parser = urlparse(url)
    if parser.scheme == '' or parser.netloc == '':
        logger.error('{} invalid url'.format(url))
        return False
    save_feed(url)
    attrs = ('item_content_xpath', 'category')
    setting = {k: v for k, v in args.items() if k in attrs and v}
    xn = args.get('removed_xpath_nodes')
    if xn:
        nodes = []
        for sn in xn.split(','):
            node = sn.strip(' \t')
            if node:
                nodes.append(node)
        if nodes:
            setting['removed_xpath_nodes'] = nodes
    if not is_exists_spider(url):
        if _gen_lxmlspider(url, setting):
            return True
    return False


@app.task(name='blogspider-creator')
def gen_blogspider(args):
    logger = get_task_logger(settings['LOGGER_NAME'])
    url = args['url']
    parser = urlparse(url)
    if parser.scheme == '' or parser.netloc == '':
        logger.error('{} invalid url'.format(url))
        return False
    save_feed(url)
    attrs = ('entry', 'item_title', 'item_link', 'item_content')
    if any(spattr not in args for spattr in attrs):
        return False
    setting = {'{}_xpath'.format(k): v
               for k, v in args.items() if k in attrs and v}
    xn = args.get('removed_xpath_nodes')
    if xn:
        nodes = []
        for sn in xn.split(','):
            node = sn.strip(' \t')
            if node:
                nodes.append(node)
        if nodes:
            setting['removed_xpath_nodes'] = nodes
    setting['name'] = get_feed_name(url)
    setting['title'] = setting['name']
    setting['category'] = args['category']
    setting['type'] = 'blog'
    setting['start_urls'] = [args['url']]
    if check_spider(setting):
        save_spider_settings(setting)
        return True
    return False


"""
task for crawl
"""


@app.task(name='crawl')
def crawl(args):
    logger = get_task_logger(settings['LOGGER_NAME'])
    logger.setLevel(settings['LOG_LEVEL'])
    logger.info('job crawl start ...')

    if not args:
        return False

    from scrapy.crawler import CrawlerProcess

    recrawl = False
    process = CrawlerProcess(settings)
    loader = process.spider_loader
    if args[0] == 'all':
        recrawl = True
        spiders = [loader.load(spid) for spid in loader.list()]
    else:
        spiders = [loader.load(spid)
                   for spid in args if spid in loader.list()]

    for sp in spiders:
        process.crawl(sp)

    def flush_db():
        conf = parse_redis_url(settings['SPIDER_STATS_URL'])
        r = redis.Redis(host=conf.host,
                        port=conf.port,
                        db=conf.database)
        r.flushdb()

    flush_db()
    process.start()

    def get_recrawl_spiders():
        if not recrawl:
            return []
        spiders = []
        conf = parse_redis_url(settings['SPIDER_STATS_URL'])
        r = redis.Redis(host=conf.host,
                        port=conf.port,
                        db=conf.database)
        for sp in loader.list():
            n = r.get(sp)
            n = 0 if n is None else int(n)
            if n == 0:
                spiders.append(sp)
        return spiders
    return get_recrawl_spiders()


@app.task(name='recrawl failed spiders')
def recrawl(spids):
    logger = get_task_logger(settings['LOGGER_NAME'])
    logger.setLevel(settings['LOG_LEVEL'])
    logger.info('recrawl job start ...')

    if not spids:
        return True

    for spid in spids:
        logger.info('error spider id: {}'.format(spid))

    from twisted.internet import reactor, defer

    @defer.inlineCallbacks
    def run_failed_spiders(settings):
        from scrapy.crawler import CrawlerRunner

        runner = CrawlerRunner(settings)
        loader = runner.spider_loader
        spiders = [loader.load(spid) for spid in spids]
        for sp in spiders:
            yield runner.crawl(sp)
        reactor.stop()
    run_failed_spiders(settings)

    reactor.run()
    return True
