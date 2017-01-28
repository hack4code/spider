# -*- coding: utf-8 -*-


import logging
import re
import uuid
from urllib.parse import urlparse

import requests
import redis
from lxml import etree

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from mydm.model import save_spider_settings, save_feed, is_exists_spider
from mydm.spiderfactory import mk_spider_cls
from mydm.util import parse_redis_url

settings = get_project_settings()
logger = logging.getLogger(__name__)


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
                        for name in names[:-1] if name.lower() != 'www'])


def check_spider(setting_):
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


def gen_lxmlspider(setting):
    url = setting['url']
    save_feed(url)
    if setting['category'] not in settings['ARTICLE_CATEGORIES']:
        logger.error((
            u'Error in gen_lxmlspider category error[{}]'
            ).format(setting['category']))
        return False
    try:
        r = requests.get(url,
                         headers=settings['DEFAULT_REQUEST_HEADERS'])
    except ConnectionError:
        logger.error((
            'Error in _gen_lxmlspider connection error[{}]'
            ).format(url))
        return False
    if r.status_code != 200:
        logger.error((
            'Error in _gen_lxmlspider requests[{},status={}]'
            ).format(url,
                     r.status_code))
        return False

    parser = etree.XMLParser(ns_clean=True)
    root = etree.XML(r.content,
                     parser)
    while len(root) == 1:
        root = root[0]
    for e in root:
        try:
            en = etree.QName(e.tag).localname.lower()
        except ValueError:
            continue
        if en == 'title':
            setting['title'] = re.sub(r'^(\r|\n|\s)+|(\r|\n|\s)+$',
                                      '',
                                      e.text)
    setting['name'] = get_feed_name(url)
    if 'title' not in setting:
        setting['title'] = setting['name']
    setting['type'] = 'xml'
    setting['start_urls'] = [url]
    del setting['url']
    if not is_exists_spider(url) and check_spider(setting):
        save_spider_settings(setting)
        return True
    else:
        logger.error('Error in gen_lxmlspider[{}]'.format(url))
        return False


def gen_blogspider(setting):
    url = setting['url']
    save_feed(url)
    if setting['category'] not in settings['ARTICLE_CATEGORIES']:
        logger.error((
            u'Error in gen_blogspider category error[{}]'
            ).format(setting['category']))
        return False
    setting['name'] = get_feed_name(url)
    setting['title'] = setting['name']
    setting['type'] = 'blog'
    setting['start_urls'] = [url]
    del setting['url']
    if not is_exists_spider(url) and check_spider(setting):
        save_spider_settings(setting)
        return True
    else:
        return False


def crawl(args):
    logger.info('job crawl start ...')
    spiders_ = args.get('spiders')
    configure_logging(settings,
                      install_root_handler=False)
    runner = CrawlerRunner(settings)
    loader = runner.spider_loader
    spiders = None
    if 'all' in spiders_:
        spiders = [loader.load(spid) for spid in loader.list()]
    else:
        spiders = [loader.load(spid) for spid in spiders_
                   if spid in loader.list()]
    if not spiders:
        return False

    for _ in spiders:
        runner.crawl(_)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    logger.info('job crawl finished')


def flush_db():
    conf = parse_redis_url(settings['SPIDER_STATS_URL'])
    r = redis.Redis(host=conf.host,
                    port=conf.port,
                    db=conf.database)
    r.flushdb()


def get_failed_spiders(loader):
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
