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


def validate_rss_feed(feed):
    url = feed['url']
    if not is_url(url):
        raise Exception(f'invalid url value[{url}]')
    if 'item_content_xpath' in feed:
        item_content_xpath = feed.get('item_content_xpath').strip('\r\n\t ')
        if not item_content_xpath:
            feed.pop('item_content_xpath')
        else:
            feed['item_content_xpath'] = item_content_xpath
    if 'removed_xpath_nodes' in feed:
        removed_xpath_nodes = feed.get('removed_xpath_nodes')
        new_removed_xpath_nodes = []
        for node in removed_xpath_nodes:
            new_node = node.strip('\r\n\t ')
            if new_node:
                new_removed_xpath_nodes.append(new_node)
        if not new_removed_xpath_nodes:
            feed.pop('removed_xpath_nodes')
        else:
            feed['removed_xpath_nodes'] = new_removed_xpath_nodes
    if 'css' in feed:
        css = feed.get('css').strip('\r\n\t ')
        if not css:
            feed.pop('css')
        else:
            feed['css'] = css


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
    save_spider_settings(feed)


def crawl(spids):
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
        logger.info("no spider found")
        return
    random.shuffle(spiders)
    # crawl process
    p = CrawlerProcess(settings)
    for spider in spiders:
        p.crawl(spider)
    logger.info('crawl job starting...')
    try:
        p.start()
    except Exception:
        logger.exception('crawl job got exception:')
    logger.info('crawl job finished')
