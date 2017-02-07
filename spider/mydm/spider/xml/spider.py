# -*- coding: utf-8 -*-


import logging

from urllib.parse import urlparse
from datetime import datetime

from lxml import etree

from scrapy.spiders import Spider
from scrapy import Request

from .extractor import ItemExtractor
from ...items import ArticleItem
from ...ai import extract_tags


logger = logging.getLogger(__name__)


class LXMLSpider(Spider):
    """
        spider crawling rss|atom
    """

    # attributes item must contain
    ATTRS = ('title',
             'link',
             'content')

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
            if all(item.get(_) is not None for _ in self.ATTRS):
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
        if all(_ in attrs for _ in ATTRS):
            bases_ = [_ for _ in bases if issubclass(_,
                                                     Spider)]
            if LXMLSpider not in bases_:
                bases_.append(LXMLSpider)
            bases_.extend([_ for _ in bases if not issubclass(_,
                                                              Spider)])
            return super().__new__(cls,
                                   name,
                                   tuple(bases_),
                                   attrs)
        else:
            miss_attrs = [_ for _ in ATTRS if _ not in attrs]
            raise AttributeError((
                'Error in LXMLSpiderMeta miss attributes{}'
                ).format(miss_attrs))
