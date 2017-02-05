# -*- coding: utf-8 -*-


import logging
import re
import json
import uuid
import random
from urllib.parse import urlparse

import requests
import redis
import pika
from lxml import etree

from twisted.internet import reactor, defer

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from mydm.model import save_spider_settings, save_feed, is_exists_spider
from mydm.spiderfactory import mk_spider_cls
from mydm.util import parse_redis_url

logger = logging.getLogger(__name__)

SETTINGS = get_project_settings()


def _send(key, data):
    body = json.dumps(data)
    connection = pika.BlockingConnection(
        pika.connection.URLParameters(SETTINGS['BROKER_URL']))
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_logs',
                             type='direct')
    channel.basic_publish(exchange='direct_logs',
                          routing_key=key,
                          body=body)
    connection.close()


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
    url = SETTINGS['TEMP_SPIDER_STATS_URL']
    TEST_SETTINGS = {'ITEM_PIPELINES': {'mydm.pipelines.StatsPipeline': 255},
                     'SPIDER_STATS_URL': url,
                     'BOT_NAME': 'TestSpider',
                     'WEBSERVICE_ENABLED': False,
                     'TELNETCONSOLE_ENABLED': False,
                     'LOG_LEVEL': 'INFO',
                     'LOG_FORMAT': '%(asctime)s-%(levelname)s: %(message)s',
                     'LOG_DATEFORMAT': '%Y-%m-%d %H:%M:%S'}

    configure_logging(TEST_SETTINGS,
                      install_root_handler=False)
    runner = CrawlerRunner(TEST_SETTINGS)
    d = runner.crawl(cls)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

    def get_stats(url, spid):
        conf = parse_redis_url(url)
        r = redis.Redis(host=conf.host,
                        port=conf.port,
                        db=conf.database)
        n = r.get(spid)
        r.delete(spid)
        return 0 if n is None else int(n)

    n = get_stats(url,
                  spid)
    return True if n > 0 else False


def gen_lxmlspider(setting):
    url = setting['url']
    del setting['url']
    save_feed(url)
    try:
        r = requests.get(url,
                         headers=SETTINGS['DEFAULT_REQUEST_HEADERS'])
    except ConnectionError:
        logger.error('Error in gen_lxmlspider connection[%s]',
                     url)
        return False
    if r.status_code != 200:
        logger.error('Error in gen_lxmlspider requests[%s, status=%d]',
                     url,
                     r.status_code)
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
        logger.error('Error in gen_lxmlspider[%s]',
                     url)
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
        logger.error('Error in gen_blogspider[%s]',
                     url)
        return False


def _get_failed_spiders(spiders):
    conf = parse_redis_url(SETTINGS['SPIDER_STATS_URL'])
    r = redis.Redis(host=conf.host,
                    port=conf.port,
                    db=conf.database)

    def get_stats(spid):
        n = r.get(spid)
        return 0 if n is None else int(n)

    return [_ for _ in spiders if not get_stats(_)]


def _flush_db():
    conf = parse_redis_url(SETTINGS['SPIDER_STATS_URL'])
    r = redis.Redis(host=conf.host,
                    port=conf.port,
                    db=conf.database)
    r.flushdb()


def crawl(args):
    spiders_ = args.get('spiders')
    spiders = []
    configure_logging(SETTINGS,
                      install_root_handler=False)
    runner = CrawlerRunner(SETTINGS)
    loader = runner.spider_loader
    if 'all' in spiders_:
        spiders = [loader.load(spid) for spid in loader.list()]
    else:
        spiders = [loader.load(spid) for spid in spiders_
                   if spid in loader.list()]
    if not spiders:
        return False

    for _ in random.sample(spiders,
                           len(spiders)):
        runner.crawl(_)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    _flush_db()
    reactor.run()

    if len(spiders) > 4:
        failed_spiders = _get_failed_spiders(spiders)
        if failed_spiders:
            _send(SETTINGS['CRAWL2_KEY'],
                  {'spiders': failed_spiders})


def crawl2(args):
    logger.info('craw2 start running ...')
    spiders = []
    spiders_ = args.get('spiders')
    configure_logging(SETTINGS,
                      install_root_handler=False)
    runner = CrawlerRunner(SETTINGS)
    loader = runner.spider_loader
    spiders = [loader.load(spid) for spid in spiders_
               if spid in loader.list()]
    if not spiders:
        return False

    @defer.inlineCallbacks
    def seq_crawl():
        for _ in random.sample(spiders,
                               len(spiders)):
            yield runner.crawl(_)
    seq_crawl()
    reactor.run()
