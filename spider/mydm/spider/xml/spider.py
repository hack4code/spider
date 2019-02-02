# -*- coding: utf-8 -*-


import logging

from urllib.parse import urlparse
from datetime import datetime

from lxml import etree

from scrapy import Request
from scrapy.spiders import Spider

from mydm.ai import extract_tags
from mydm.items import ArticleItem
from mydm.spider.spider import ErrbackSpider
from .extractor import ItemExtractor


logger = logging.getLogger(__name__)

XMLSPIDER_ATTRS = ['start_urls', 'category', 'name']


def set_item_tag(txt, item, encoding='utf-8'):
    tags = extract_tags(txt, encoding)
    if tags:
        item['tag'] = tags


class LXMLSpider(Spider):
    """
        spider crawling rss|atom
    """

    # attributes must contain
    ATTRS = ('title', 'link')

    def extract_content(self, response):
        item = response.meta['item']
        content = response.xpath(self.item_content_xpath).extract_first()
        if not content:
            logger.error(
                    'spider[%s] extract content failed[%s]',
                    self.name,
                    response.url
            )
            return
        item['content'] = content
        item['encoding'] = response.encoding
        item['link'] = response.url
        if item.get('tag') is None:
            set_item_tag(content, item, item['encoding'])
        return ArticleItem(item)

    def parse(self, response):
        parser = etree.XMLParser(
                ns_clean=True,
                recover=True,
                encoding=response.encoding
        )
        root = etree.XML(response.body, parser)
        if root is None:
            logger.error('spider[%s] rss feed parse failed', self.name)
            yield None
        else:
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
                if all(item.get(attr) is not None for attr in self.ATTRS):
                    if (item.get('tag') is None and
                            item.get('content') is not None):
                        set_item_tag(item['content'], item, item['encoding'])
                    if hasattr(self, 'item_content_xpath'):
                        try:
                            link = '{}?{}'.format(
                                    item['link'],
                                    self.item_content_link_parameter
                                    )
                        except AttributeError:
                            link = item['link']
                        yield Request(
                                link,
                                meta={'item': item},
                                callback=self.extract_content,
                                errback=self.errback,
                                dont_filter=True
                        )
                    elif item.get('content'):
                        yield ArticleItem(item)


class LXMLSpiderMeta(type):

    def __new__(cls, name, bases, attrs):
        if all(attr in attrs for attr in XMLSPIDER_ATTRS):

            def update_bases(bases):
                new_bases = [LXMLSpider]
                new_bases.extend(bases)
                if ErrbackSpider not in new_bases:
                    new_bases.append(ErrbackSpider)
                return tuple(new_bases)

            bases = update_bases(bases)
            return super().__new__(
                    cls,
                    name,
                    bases,
                    attrs
            )
        else:
            miss_attrs = [
                    attr
                    for attr in XMLSPIDER_ATTRS
                    if attr not in attrs
            ]
            raise AttributeError(f'miss attributes[{miss_attrs}]')
