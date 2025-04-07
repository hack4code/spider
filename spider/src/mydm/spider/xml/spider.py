# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from urllib.parse import urlparse

from lxml import etree

from scrapy import Request
from scrapy.spiders import Spider

from mydm.items import ArticleItem
from .extractor import ItemExtractor
from mydm.spider.spider import ErrbackSpider
from mydm.spidermeta import SpiderMeta
from mydm.utils import extract_tags, extract_head


logger = logging.getLogger(__name__)


class LXMLSpider(Spider):
    """ spider attribute:
    start_urls
        category
        name
        item_content_xpath
        item_content_link_parameter
    """

    def extract_item_tags(self, item, *, response=None):
        if 'tag' in item:
            return
        if 'content' not in item:
            return
        tags = extract_tags(item['content'], item['encoding'])
        if not tags:
            return
        logger.info(
            'spider[%s] extract tags %s',
            self.name,
            tags
        )
        item['tag'] = tags

    def extract_item_head(self, item, *, response=None):
        head = extract_head(response)
        if head:
            item['head'] = head

    def extract_head(self, response):
        item = response.meta['item']
        self.extract_item_head(item, response=response)
        return ArticleItem(item)

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
        self.extract_item_head(item, response=response)
        self.extract_item_tags(item)
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
                item = ItemExtractor()(entry)
                item['category'] = self.title
                item['crawl_date'] = datetime.now()
                item['domain'] = urlparse(response.request.url).netloc
                item['data_type'] = 'html'
                item['encoding'] = response.encoding
                if any(item.get(attr) is None for attr in ('title', 'link')):
                    continue
                self.extract_item_tags(item)
                try:
                    params = self.item_content_link_parameter
                except AttributeError:
                    link = item['link']
                else:
                    link = f'{item["link"]}?{params}'
                if hasattr(self, 'item_content_xpath'):
                    yield Request(
                        link,
                        meta={'item': item},
                        callback=self.extract_content,
                        errback=self.errback,
                        dont_filter=True
                    )
                elif item.get('content'):
                    yield Request(
                        link,
                        meta={'item': item},
                        callback=self.extract_head,
                        errback=self.errback,
                        dont_filter=True
                    )


class LXMLSpiderMeta(SpiderMeta, type, spider_type='xml'):
    SPIDER_ATTRS = ('start_urls', 'category', 'name', 'title')

    def __new__(cls, name, bases, attrs):
        if all(attr in attrs for attr in cls.SPIDER_ATTRS):
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
                for attr in cls.SPIDER_ATTRS
                if attr not in attrs
            ]
            raise AttributeError(f'miss attributes{miss_attrs}')
