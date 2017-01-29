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
    fields = parser.hostname.split('.')
    if len(fields) == 1:
        return re.sub(r'[^a-zA-Z]',
                      '',
                      fields[0]
                      ).lower().capitalize()
    else:
        return ''.join([re.sub(r'[^a-zA-Z]',
                               '',
                               _).lower().capitalize()
                        for _ in fields[:-1] if _.lower() != 'www'])


def test_spider(setting):
    setting = setting.copy()
    spid = str(uuid.uuid4())
    setting['_id'] = spid
    cls = mk_spider_cls(setting)
    url = settings['TEMP_SPIDER_STATS_URL']
    test_settings = {'ITEM_PIPELINES': {'mydm.pipelines.StatsPipeline': 255},
                     'SPIDER_STATS_URL': url}

    p = CrawlerProcess(test_settings)
    p.crawl(cls)
    p.start()

    def get_stats(url, spid):
        conf = parse_redis_url(url)
        r = redis.Redis(host=conf.host,
                        port=conf.port,
                        db=conf.database)
        n = r.get(spid)
        r.delete(spid)
        return 0 if n is None else int(n)

    n = get_stats(url, spid)
    return True if n > 0 else False


def gen_lxmlspider(setting):
    url = setting['url']
    del setting['url']
    save_feed(url)
    try:
        r = requests.get(url,
                         headers=settings['DEFAULT_REQUEST_HEADERS'])
    except ConnectionError:
        logger.error((
            'Error in gen_lxmlspider connection[{}]'
            ).format(url))
        return False
    if r.status_code != 200:
        logger.error((
            'Error in gen_lxmlspider requests[{}, status={}]'
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
        else:
            if en == 'title':
                setting['title'] = re.sub(r'^(\r|\n|\s)+|(\r|\n|\s)+$',
                                          '',
                                          e.text)
    setting['name'] = get_feed_name(url)
    if 'title' not in setting:
        setting['title'] = setting['name']
    setting['type'] = 'xml'
    setting['start_urls'] = [url]
    if is_exists_spider(url):
        return True
    if test_spider(setting):
        save_spider_settings(setting)
        return True
    else:
        logger.error('Error in gen_lxmlspider[{}]'.format(url))
        return False


def gen_blogspider(setting):
    url = setting['url']
    del setting['url']
    save_feed(url)
    setting['name'] = get_feed_name(url)
    setting['title'] = setting['name']
    setting['type'] = 'blog'
    setting['start_urls'] = [url]
    if is_exists_spider(url):
        return True
    if test_spider(setting):
        save_spider_settings(setting)
        return True
    else:
        logger.error('Error in gen_blogspider[{}]'.format(url))
        return False


def crawl(args):
    spiders_ = args.get('spiders')
    spiders = []
    configure_logging(settings,
                      install_root_handler=False)
    runner = CrawlerRunner(settings)
    loader = runner.spider_loader
    if 'all' in spiders_:
        spiders = [loader.load(spid) for spid in loader.list()]
    else:
        spiders = [loader.load(spid) for spid in spiders_
                   if spid in loader.list()]
    if not spiders:
        return False
    for sp in spiders:
        runner.crawl(sp)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


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
