# -*- coding: utf-8 -*-


import logging
import re
import uuid
import random
from urllib.parse import urlparse
from multiprocessing import Process

import requests
from lxml import etree

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from mydm.spiderfactory import SpiderFactory
from mydm.spiderloader import MongoSpiderLoader
from mydm.model import save_spider_settings
from mydm.utils import is_url


logger = logging.getLogger(__name__)
TEST_SETTINGS = {
    'ITEM_PIPELINES': {},
    'DOWNLOADER_MIDDLEWARES': {},
    'BOT_NAME': 'TestSpider',
    'WEBSERVICE_ENABLED': False,
    'TELNETCONSOLE_ENABLED': False,
    'LOG_LEVEL': 'WARNING',
    'LOG_FORMAT': '%(asctime)s-%(levelname)s: %(message)s',
    'LOG_DATEFORMAT': '%Y-%m-%d %H:%M:%S'
}


def get_feed_name(url):
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
                re.sub(r'[^a-zA-Z]', '', item).lower().capitalize()
                for item in fields[:-1]
                if item.lower() != 'www'
        )


def run_feed_spider(url, feed):
    spid = str(uuid.uuid4())
    feed['_id'] = spid
    cls = SpiderFactory.create_spider(feed)
    proc = CrawlerProcess(TEST_SETTINGS)
    proc.start()
    del feed['_id']


def dry_run_feed_spider(url, feed):
    p = Process(target=run_feed_spider, args=(url, feed))
    p.start()
    p.join()
    return p.exitcode == 0


def validate_rss_feed(feed):
    url = feed['url']
    if not is_url(url):
        raise Exception(f'invalid url value[{url}]')
    item_content_xpath = feed['item_content_xpath'].strip('\r\n\t ')
    if not item_content_xpath:
        feed.pop('item_content_xpath')
    else:
        feed['item_content_xpath'] = item_content_xpath
    removed_xpath_nodes = feed['removed_xpath_nodes']
    new_removed_xpath_nodes = []
    for node in removed_xpath_nodes:
        new_node = node.strip('\r\n\t ')
        if new_node:
            new_removed_xpath_nodes.append(new_node)
    if not new_removed_xpath_nodes:
        feed.pop('removed_xpath_nodes')
    else:
        feed['removed_xpath_nodes'] = new_removed_xpath_nodes


def submit_rss_feed(feed):
    validate_rss_feed(feed)
    url = feed.pop('url')
    settings = get_project_settings()
    headers = settings['DEFAULT_REQUEST_HEADERS'].copy()
    headers['User-Agent'] = settings['USER_AGENT']
    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError:
        logger.error('rss spider connect %s failed', url)
        raise
    if r.status_code != 200:
        logger.error(
                'rss spider got bad response[%s, status=%d]',
                url,
                r.status_code
        )
        raise Exception(f'bad response for rss feed[{url}]')

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
        logger.error('rss feed[%s] parse failed', url)
        raise

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
            feed['title'] = re.sub(
                    r'^(\r|\n|\s)+|(\r|\n|\s)+$',
                    '',
                    e.text
            )
    feed['name'] = get_feed_name(url)
    if 'title' not in feed:
        feed['title'] = feed['name']
    feed['type'] = 'xml'
    feed['start_urls'] = [url]
    try:
        success = dry_run_feed_spider(url, feed)
    except:
        raise Exception('spider dry run failed')
    if not success:
        raise Exception('spider dry run failed')
    save_spider_settings(feed)


def validate_blog_feed(feed):
    url = feed['url']
    if not is_url(url):
        raise Exception(f'invalid url value[{url}]')
    category = feed['category'].strip('\r\n\t ')
    if not category:
        raise Exception('category value is empty')
    else:
        feed['category'] = category
    entry_xpath = feed['entry_xpath'].strip('\r\n\t ')
    if not entry_xpath:
        raise Exception('entry_xpath value is empty')
    else:
        feed['entry_xpath'] = entry_xpath
    item_title_xpath = feed['item_title_xpath'].strip('\r\n\t ')
    if not item_title_xpath:
        raise Exception('item_title_xpath value is empty')
    else:
        feed['item_title_xpath'] = item_title_xpath
    item_link_xpath = feed['item_link_xpath'].strip('\r\n\t ')
    if not item_link_xpath:
        raise Exception('item_link_xpath value is empty')
    else:
        feed['item_link_xpath'] = item_link_xpath
    item_content_xpath = feed['item_content_xpath'].strip('\r\n\t ')
    if not item_content_xpath:
        raise Exception('item_content_xpath value is empty')
    else:
        feed['item_content_xpath'] = item_content_xpath
    removed_xpath_nodes = feed['removed_xpath_nodes']
    new_removed_xpath_nodes = []
    for node in removed_xpath_nodes:
        new_node = node.strip('\r\n\t ')
        if new_node:
            new_removed_xpath_nodes.append(new_node)
    if not new_removed_xpath_nodes:
        feed.pop('removed_xpath_nodes')
    else:
        feed['removed_xpath_nodes'] = new_removed_xpath_nodes


def submit_blog_feed(feed):
    validate_blog_feed(feed)
    url = feed.pop('url')
    feed['name'] = get_feed_name(url)
    feed['title'] = feed['name']
    feed['type'] = 'blog'
    feed['start_urls'] = [url]
    try:
        success = dry_run_feed_spider(url, feed)
    except:
        raise Exception('spider dry run failed')
    if not success:
        raise Exception('spider dry run failed')
    save_spider_settings(feed)


def crawl_articles(spids):
    settings = get_project_settings()
    loader = MongoSpiderLoader.from_settings(settings)
    if 'all' in spids:
        spids = loader.list()
    spiders = [
        loader.load(spid)
        for spid in spids
        if spid in loader.list()
    ]
    if not spiders:
        return
    random.shuffle(spiders)
    # crawl process
    proc = CrawlerProcess(settings)
    for spider in spiders:
        proc.crawl(spider)
    logger.info('crawl job starting...')
    try:
        proc.start()
    except Exception:
        logger.exception('crawl job got exception:')
    logger.info('crawl job finished')
