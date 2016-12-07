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
        return re.sub(r'[^a-zA-Z]', '', names[0]).capitalize()
    else:
        return ''.join([re.sub(r'[^a-z]', '', name.lower()).capitalize()
                        for name in names[:-1]
                        if name.lower() != 'www'])


def check_spider(sp_setting):
    import uuid
    from scrapy.crawler import CrawlerProcess

    spid = str(uuid.uuid4())
    sp_setting['_id'] = spid
    spcls = mk_spider_cls(sp_setting)
    custom_settings = {'ITEM_PIPELINES': {'mydm.pipelines.StatsPipeline':
                                          255},
                       'WEBSERVICE_ENABLED': False,
                       'TELNETCONSOLE_ENABLED': False,
                       'LOG_LEVEL': 'INFO',
                       'LOG_STDOUT': True,
                       'LOG_ENABLED': True,
                       'SPIDER_STATS_URL': settings['TEMP_SPIDER_STATS_URL']}

    p = CrawlerProcess(custom_settings)
    p.crawl(spcls)
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
    logger = get_task_logger(__name__)
    r = requests.get(url, headers=settings['DEFAULT_REQUEST_HEADERS'])
    if r.status_code != 200:
        logger.error('download {} error: status={}'.format(url, r.status_code))
        return False
    parser = etree.XMLParser(ns_clean=True)
    root = etree.XML(r.content, parser)
    while len(root) == 1:
        root = root[0]
    sp_setting = {'start_urls': [url]}
    for e in root:
        try:
            en = QName(e.tag).localname.lower()
        except ValueError:
            continue
        if en == 'title':
            sp_setting['title'] = re.sub(r'^(\r|\n|\s)+|(\r|\n|\s)+$',
                                         '',
                                         e.text)
    sp_setting['name'] = get_feed_name(url)
    if 'title' not in sp_setting:
        sp_setting['title'] = sp_setting['name']
    sp_setting['category'] = args['category']
    if sp_setting['category'] not in settings['ARTICLE_CATEGORIES']:
        logger.error(u'{} category error'.format(sp_setting['category']))
        return False
    spattrs = ('item_content_xpath', 'removed_xpath_nodes')
    sp_setting.update({k: args[k] for k in spattrs if k in args})
    sp_setting['type'] = 'xml'
    if check_spider(sp_setting):
        save_spider_settings(sp_setting)
        return True
    logger.error('gen_lxmlspider error for {}'.format(url))
    return False


@app.task(name='lxmlspider-creator')
def gen_lxmlspider(spargs):
    logger = get_task_logger(__name__)
    url = spargs['url']
    logger.info('gen_lxmlspider for {}'.format(url))
    parser = urlparse(url)
    if parser.scheme == '' or parser.netloc == '':
        logger.error('{} invalid url'.format(url))
        return False
    save_feed(url)
    spattrs = ('item_content_xpath', 'category')
    args = {k: v for k, v in spargs.items() if k in spattrs and len(v) > 0}
    if ('removed_xpath_nodes' in spargs
       and len(spargs['removed_xpath_nodes']) > 0):
        nodes = [n.strip() for n in spargs['removed_xpath_nodes'].split(',')]
        args['item_content_xpath'] = nodes
    if not is_exists_spider(url):
        if _gen_lxmlspider(url, args):
            return True
    return False


@app.task(name='blogspider-creator')
def gen_blogspider(spargs):
    logger = get_task_logger(__name__)
    url = spargs['url']
    parser = urlparse(url)
    if parser.scheme == '' or parser.netloc == '':
        logger.error('{} invalid url'.format(url))
        return False
    save_feed(url)
    spattrs = ('entry', 'item_title', 'item_link', 'item_content')
    if any(spattr not in spargs for spattr in spattrs):
        return False
    sp_setting = {'{}_xpath'.format(k): v
                  for k, v in spargs.items() if k in spattrs and len(v) > 0}
    if 'removed_xpath_nodes' in spargs and spargs['removed_xpath_nodes'] > 0:
        nodes = [n.strip() for n in spargs['removed_xpath_nodes'].split(',')]
        sp_setting['removed_xpath_nodes'] = nodes
    sp_setting['name'] = get_feed_name(url)
    sp_setting['title'] = sp_setting['name']
    sp_setting['category'] = spargs['category']
    sp_setting['type'] = 'blog'
    sp_setting['start_urls'] = [spargs['url']]
    if check_spider(sp_setting):
        save_spider_settings(sp_setting)
        return True
    return False


"""
task for crawl
"""


@app.task(name='crawl')
def crawl(args):
    logger = get_task_logger(__name__)
    logger.info('job crawl start ...')

    if len(args) == 0:
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

    def flush_spider_stats_db():
        conf = parse_redis_url(settings['SPIDER_STATS_URL'])
        r = redis.Redis(host=conf.host, port=conf.port, db=conf.database)
        r.flushdb()

    flush_spider_stats_db()
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
    logger = get_task_logger(__name__)
    logger.info('recrawl job start ...')

    if spids is None or len(spids) == 0:
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
