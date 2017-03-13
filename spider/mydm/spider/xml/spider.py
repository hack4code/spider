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
from ...ai import extract_tags


logger = logging.getLogger(__name__)
XMLSPIDER_ATTRS = ['start_urls', 'category', 'name']


def set_item_tag(txt, item, encoding='utf-8'):
    tags = extract_tags(txt,
                        encoding)
    if tags:
        item['tag'] = tags


class LXMLSpider(Spider):
    """
        spider crawling rss|atom
    """

    # attributes must contain
    ATTRS = ('title',
             'link')

    def extract_content(self, response):
        item = response.meta['item']
        content = response.xpath(self.item_content_xpath).extract_first()
        if content is not None:
            item['content'] = content
            item['encoding'] = response.encoding
            item['link'] = response.url
            if item.get('tag') is None:
                set_item_tag(content,
                             item,
                             item['encoding'])
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
                if item.get('tag') is None and item.get('content') is not None:
                    set_item_tag(item['content'],
                                 item,
                                 item['encoding'])
                if hasattr(self,
                           'item_content_xpath'):
                    try:
                        link = '{}?{}'.format(item['link'],
                                              self.item_content_link_parameter)
                    except AttributeError:
                        link = item['link']
                    yield Request(link,
                                  meta={'item': item},
                                  callback=self.extract_content,
                                  errback=self.errback,
                                  dont_filter=True)
                elif item.get('content') is not None:
                    yield ArticleItem(item)


class LXMLSpiderMeta(type):
    def __new__(cls, name, bases, attrs):
        if all(_ in attrs for _ in XMLSPIDER_ATTRS):
            def update_bases(bases):
                assert LXMLSpider not in bases, 'LXMLSpider in bases'
                bases_ = [LXMLSpider]
                bases_.extend(bases)
                if ErrbackSpider not in bases_:
                    bases_.append(ErrbackSpider)
                return tuple(bases_)
            bases = update_bases(bases)
            return super().__new__(cls,
                                   name,
                                   bases,
                                   attrs)
        else:
            miss_attrs = [_ for _ in XMLSPIDER_ATTRS if _ not in attrs]
            raise AttributeError((
                'Error in LXMLSpiderMeta miss attributes{}'
                ).format(miss_attrs))
