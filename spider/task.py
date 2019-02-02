# -*- coding: utf-8 -*-


import logging
import re
import json
import uuid
import random
from urllib.parse import urlparse

import requests
import pika
from lxml import etree

from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from mydm.spiderfactory import SpiderFactory
from mydm.exceptions import SpiderFactoryException
from mydm.model import (
        save_spider_settings, save_feed, is_exists_spider, get_stats
)


logger = logging.getLogger(__name__)
SETTINGS = get_project_settings()


def _send(key, data):
    body = json.dumps(data)
    connection = pika.BlockingConnection(
        pika.connection.URLParameters(SETTINGS['BROKER_URL'])
    )
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_logs', type='direct')
    channel.basic_publish(
            exchange='direct_logs',
            routing_key=key,
            body=body
    )
    connection.close()


def _get_feed_name(url):
    parser = urlparse(url)
    fields = parser.hostname.split('.')
    if len(fields) == 1:
        return re.sub(
                r'[^a-zA-Z]',
                '',
                fields[0]
        ).lower().capitalize()
    else:
        return ''.join(
                re.sub(r'[^a-zA-Z]', '', _).lower().capitalize()
                for _ in fields[:-1]
                if _.lower() != 'www'
        )


def test_spider(setting):
    setting = setting.copy()
    spid = str(uuid.uuid4())
    setting['_id'] = spid
    try:
        cls = SpiderFactory.mkspider(setting)
    except SpiderFactoryException as e:
        logger.error('Error in test_spider SpiderFactory[%s]', e)
        return False
    TEST_SETTINGS = {
        'EXTENSIONS': {
            'mydm.extensions.ExtensionStats': 900,
            'scrapy.extensions.logstats.LogStats': None,
            'scrapy.extensions.spiderstate.SpiderState': None,
            'scrapy.extensions.telnet.TelnetConsole': None,
        },
        'BOT_NAME': 'TestSpider',
        'WEBSERVICE_ENABLED': False,
        'TELNETCONSOLE_ENABLED': False,
        'LOG_LEVEL': 'INFO',
        'LOG_FORMAT': '%(asctime)s-%(levelname)s: %(message)s',
        'LOG_DATEFORMAT': '%Y-%m-%d %H:%M:%S'
    }

    configure_logging(TEST_SETTINGS, install_root_handler=False)
    logging.getLogger('scrapy').setLevel(logging.WARNING)
    runner = CrawlerRunner(TEST_SETTINGS)
    d = runner.crawl(cls)
    d.addBoth(lambda _: reactor.stop())
    logger.info('test_spider reator starting ...')
    reactor.run()
    logger.info('test_spider reator stopped')
    stats = get_stats([spid])
    n = stats[spid]
    return True if n > 0 else False


def gen_lxmlspider(setting):
    url = setting['url']
    del setting['url']
    save_feed(url)
    headers = SETTINGS['DEFAULT_REQUEST_HEADERS'].copy()
    headers['User-Agent'] = SETTINGS['USER_AGENT']
    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError:
        logger.error('Error in gen_lxmlspider connection[%s]', url)
        return False
    if r.status_code != 200:
        logger.error(
                'Error in gen_lxmlspider requests[%s, status=%d]',
                url,
                r.status_code
        )
        return False

    parser = etree.XMLParser(
            encoding=r.encoding,
            ns_clean=True,
            remove_blank_text=True,
            dtd_validation=False,
            load_dtd=True
    )
    try:
        root = etree.XML(r.content, parser)
    except Exception:
        logger.exception('Error in gen_lxmlspider parse feed[%s] failed', url)
        return False

    while len(root) == 1:
        root = root[0]
    for e in root:
        try:
            en = etree.QName(e.tag).localname.lower()
        except ValueError:
            continue
        else:
            if en != 'title':
                continue
            setting['title'] = re.sub(
                    r'^(\r|\n|\s)+|(\r|\n|\s)+$',
                    '',
                    e.text
            )
    setting['name'] = _get_feed_name(url)
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
        logger.error('Error in gen_lxmlspider[%s]', url)
        return False


def gen_blogspider(setting):
    url = setting['url']
    del setting['url']
    save_feed(url)
    setting['name'] = _get_feed_name(url)
    setting['title'] = setting['name']
    setting['type'] = 'blog'
    setting['start_urls'] = [url]
    if is_exists_spider(url):
        return True
    if test_spider(setting):
        save_spider_settings(setting)
        return True
    else:
        logger.error('Error in gen_blogspider[%s]', url)
        return False


def crawl(args):
    spids = args.get('spiders')
    configure_logging(SETTINGS, install_root_handler=False)
    logging.getLogger('scrapy').setLevel(logging.WARNING)
    runner = CrawlerRunner(SETTINGS)
    loader = runner.spider_loader
    if 'all' in spids:
        spids = loader.list()
    spiders = [
        loader.load(spid)
        for spid in spids
        if spid in loader.list()
    ]
    if not spiders:
        return False

    random.shuffle(spiders)
    for spider in spiders:
        runner.crawl(spider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    logger.info('crawl reator starting...')
    reactor.run()
    logging.info('crawl reator stopped')
