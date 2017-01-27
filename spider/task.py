# -*- coding: utf-8 -*-


import logging
import re
import uuid
from urllib.parse import urlparse

import requests
import redis

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
                        for name in names[:-1]
                        if name.lower() != 'www'])


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


def _gen_lxmlspider(url, args):
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

    from lxml import etree
    parser = etree.XMLParser(ns_clean=True)
    root = etree.XML(r.content,
                     parser)
    while len(root) == 1:
        root = root[0]
    setting = {'start_urls': [url]}
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
    logger.error('Error in gen_lxmlspider[{}]'.format(url))
    return False


def _set_removed_xpath_nodes(args, setting):
    removed_xpath_nodes_ = args.get('removed_xpath_nodes', None)
    if removed_xpath_nodes_:
        removed_xpath_nodes = [_ for _ in (__.strip(' \t\r\n')
                                           for __ in removed_xpath_nodes_)
                               if _]
        if removed_xpath_nodes:
            settings['removed_xpath_nodes'] = removed_xpath_nodes


def _check_url(url):
    parser = urlparse(url)
    if not parser.scheme or not parser.netloc:
        return False
    return True


def gen_lxmlspider(args):
    url = args['url']
    if not _check_url(url):
        logger.error('Error in gen_lxmlspider invalid url[{}]'.format(url))
        return False

    save_feed(url)

    attrs = ('item_content_xpath', 'category')
    setting = {k: v for k, v in args.items() if k in attrs and v}
    _set_removed_xpath_nodes(args, setting)

    if not is_exists_spider(url):
        if _gen_lxmlspider(url, setting):
            return True
    return False


def gen_blogspider(args):
    url = args['url']
    if not _check_url(url):
        logger.error('Error in gen_blogspider invalid url[{}]'.format(url))
        return False

    save_feed(url)

    attrs = ('entry_xpath',
             'item_title_xpath',
             'item_link_xpath',
             'item_content_xpath')
    if any(attr not in args for attr in attrs):
        logger.error('Error in gen_blogspider xpath field')
        return False
    setting = {k: v for k, v in args.items() if k in attrs and v}
    _set_removed_xpath_nodes(args, setting)
    setting['name'] = get_feed_name(url)
    setting['title'] = setting['name']
    setting['category'] = args['category']
    setting['type'] = 'blog'
    setting['start_urls'] = [args['url']]
    if check_spider(setting):
        save_spider_settings(setting)
        return True
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


def flush_db():
    conf = parse_redis_url(settings['SPIDER_STATS_URL'])
    r = redis.Redis(host=conf.host,
                    port=conf.port,
                    db=conf.database)
    r.flushdb()


def get_recrawl_spiders(loader):
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
