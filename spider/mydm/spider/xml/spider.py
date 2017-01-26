# -*- coding: utf-8 -*-


import logging

from urllib.parse import urlparse
from datetime import datetime

from lxml import etree

from scrapy.spiders import Spider
from scrapy import Request

from .extractor import ItemExtractor
from ..spider import ErrbackSpider
from ...items import ArticleItem


logger = logging.getLogger(__name__)


def extract_tags(doc, encoding):
    from ...ai import TagExtractor
    extract = TagExtractor()
    return extract(doc, encoding=encoding)


class LXMLSpider(Spider):
    """
        spider for crawl rss|atom
    """

    # Tags item must contain
    TAGS = ('title', 'link', 'content')

    def check_item(self, item):
        return True if all(k in item and item[k] is not None
                           for k in self.TAGS) else False

    def extract_content(self, response):
        item = response.meta['item']
        content = response.xpath(self.item_content_xpath).extract_first()
        if content is not None:
            item['content'] = content
            item['encoding'] = response.encoding
            item['link'] = response.url
            if 'tag' not in item:
                tags = extract_tags(item['content'],
                                    item['encoding'])
                if tags is not None:
                    item['tag'] = tags
            return ArticleItem(item)
        else:
            logger.error('spider[{}] extract content failed'.format(self.name))
            return None

    def parse(self, response):
        parser = etree.XMLParser(ns_clean=True,
                                 recover=True,
                                 encoding=response.encoding)
        root = etree.XML(response.body,
                         parser)
        while len(root) == 1:
            root = root[0]
        for entry in root:
            extract = ItemExtractor()
            item = extract(entry)
            item['category'] = self.category
            item['crawl_date'] = datetime.now()
            item['domain'] = urlparse(response.request.url).netloc
            item['data_type'] = 'html'
            item['encoding'] = response.encoding
            if self.check_item(item):
                if hasattr(self,
                           'item_content_xpath'):
                    yield Request(item['link'],
                                  callback=self.extract_content,
                                  errback=self.errback,
                                  meta={'item': item})
                else:
                    if 'tag' not in item:
                        tags = extract_tags(item['content'],
                                            item['encoding'])
                        if tags is not None:
                            item['tag'] = tags
                    yield ArticleItem(item)


class LXMLSpiderMeta(type):
    def __new__(cls, name, bases, attrs):
        ATTRS = ['start_urls',
                 'category',
                 'name']
        if all(attr in attrs for attr in ATTRS):
            return super(LXMLSpiderMeta,
                         cls).__new__(cls,
                                      name,
                                      bases,
                                      attrs)
        else:
            raise AttributeError('Error in LXMLSpiderMeta')


def mk_lxmlspider_cls(setting):
    return LXMLSpiderMeta('{}Spider'.format(setting['name'].capitalize()),
                          (LXMLSpider, ErrbackSpider),
                          setting)
