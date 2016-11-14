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


def get_stats(custom_settings):
    conf = parse_redis_url(custom_settings['STATS_URL'])
    r = redis.Redis(host=conf.host, port=conf.port, db=conf.database)
    key = custom_settings['STATS_KEY']
    return int(r.get(key))


def check_spider(sp_setting):
    from scrapy.crawler import CrawlerProcess

    spcls = mk_spider_cls(sp_setting)
    custom_settings = {'ITEM_PIPELINES': {'mydm.pipelines.CountPipeline':
                                          255},
                       'WEBSERVICE_ENABLED': False,
                       'TELNETCONSOLE_ENABLED': False,
                       'LOG_LEVEL': 'INFO',
                       'LOG_STDOUT': True,
                       'LOG_ENABLED': True,
                       'STATS_URL': settings['TEMP_SPIDER_STATS_URL'],
                       'STATS_KEY': str(id(spcls))}

    p = CrawlerProcess(custom_settings)
    p.crawl(spcls)
    p.start()
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
    if 'item_content_xpath' in args:
        sp_setting['item_content_xpath'] = args['item_content_xpath']
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
    args = {k: v for k, v in spargs.items() if v != ''}
    if 'content' in spargs and len(spargs['content']) > 0:
        args['item_content_xpath'] = spargs['content']
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
                  for k, v in spargs.items() if k in spattrs}
    if 'removed_xpath_nodes' in spargs:
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


@app.task(name='crawl-job')
def crawl(args):
    if len(args) == 0:
        return False

    def init_logger(settings):
        import logging
        logger = get_task_logger(__name__)
        LEVELS = {'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARNING': logging.WARNING,
                  'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}
        logger.setLevel(LEVELS[settings['LOG_LEVEL']])
        from scrapy.utils.log import configure_logging
        configure_logging(settings, install_root_handler=False)

    init_logger(settings)

    from twisted.internet import reactor

    def run_spiders(settings):
        from scrapy.crawler import CrawlerRunner

        runner = CrawlerRunner(settings)
        loader = runner.spider_loader
        if args[0] == 'all':
            spiders = [loader.load(spid) for spid in loader.list()]
        else:
            spiders = [loader.load(spid)
                       for spid in args if spid in loader.list()]

        map(lambda sp: runner.crawl(sp), spiders)
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())

    run_spiders(settings)
    reactor.run()
    return True
