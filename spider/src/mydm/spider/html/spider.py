# -*- coding: utf-8 -*-


import logging
from html import unescape
from datetime import datetime
from urllib.parse import urlparse

from scrapy import Request
from scrapy.spiders import Spider

from mydm.items import ArticleItem
from mydm.spider.spider import ErrbackSpider
from mydm.spiderfactory import SpiderFactory
from mydm.ai import extract_tags, extract_head


logger = logging.getLogger(__name__)


class BLOGSpider(Spider):

    def extract_item_head(self, item, *, response=None):
        head = extract_head(response)
        if not head:
            return
        item['head'] = head

    def extract_item_tags(self, item, *, content=None):
        if 'tag' in item:
            return
        if 'content' not in item:
            return
        if content is None:
            content = item['content']
        tags = extract_tags(content, item['encoding'])
        if not tags:
            return
        logger.info(
                'spider[%s] extract tags %s',
                self.name,
                tags
        )
        item['tag'] = tags

    def extract_entries(self, response):
        return response.selector.xpath(self.entry_xpath)

    def extract_item(self, entry, encoding):
        item = {
                attr: entry.xpath(xpath).extract_first()
                for attr, xpath in self.item_extractors
        }
        item['encoding'] = encoding
        self.extract_item_tags(
                item,
                content=entry.xpath('.').extract_first()
        )
        if item.get('link') is not None:
            item['link'] = item['link'].strip('\t\n\r ')
        if item.get('title') is not None:
            item['title'] = unescape(item['title'])
        return item

    def extract_content(self, response):
        ITEM_KEYS = ('title', 'link', 'content')
        item = response.meta['item']
        item['encoding'] = response.encoding
        item['link'] = response.url.strip('\t\n\r ')
        self.extract_item_head(item, response=response)
        content = response.xpath(self.item_content_xpath).extract_first()
        item['content'] = content
        self.extract_item_tags(item)
        if all(item.get(attr) is not None for attr in ITEM_KEYS):
            return ArticleItem(item)
        else:
            miss_keys = [
                    attr
                    for attr in ITEM_KEYS
                    if item.get(attr) is None
            ]
            logger.error(
                    'spider[%s] extract content miss keys%s',
                    self.name,
                    miss_keys
            )

    def parse(self, response):
        try:
            xplink = self.link_pre_xpath
        except AttributeError:
            pass
        else:
            prelink = response.xpath(xplink).extract_first()
            yield Request(
                    prelink,
                    callback=self.parse,
                    errback=self.errback
            )

        for entry in self.extract_entries(response):
            item = self.extract_item(entry, response.encoding)
            item['category'] = self.category
            item['crawl_date'] = datetime.now()
            item['domain'] = urlparse(response.request.url).netloc
            item['data_type'] = 'html'
            link = item.get('link')
            if link is None:
                continue
            if not link.startswith('http'):
                item['link'] = response.urljoin(link)
            yield Request(
                    item['link'],
                    meta={'item': item},
                    callback=self.extract_content,
                    errback=self.errback,
                    dont_filter=True
            )


class BLOGSpiderMeta(SpiderFactory, type, spider_type='blog'):

    SPIDER_ATTRS = (
            'start_urls',
            'category',
            'entry_xpath',
            'item_title_xpath',
            'item_link_xpath',
            'item_content_xpath'
    )

    def __new__(cls, name, bases, attrs):
        if all(attr in attrs for attr in cls.SPIDER_ATTRS):

            def update_bases(bases):
                new_bases = [BLOGSpider]
                new_bases.extend(bases)
                if ErrbackSpider not in new_bases:
                    new_bases.append(ErrbackSpider)
                return tuple(new_bases)

            def update_attrs(attrs):
                new_attrs = attrs.copy()
                extractors = []
                for k, v in new_attrs.items():
                    fields = k.split('_')
                    if (len(fields) == 3 and fields[0] == 'item' and
                            fields[1] != 'content' and fields[2] == 'xpath'):
                        extractors.append((fields[1], v))
                new_attrs['item_extractors'] = tuple(extractors)
                for k, _ in extractors:
                    del new_attrs[f'item_{k}_xpath']
                return new_attrs

            bases = update_bases(bases)
            attrs = update_attrs(attrs)
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
