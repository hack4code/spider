# -*- coding: utf-8 -*-


import logging
from html import unescape
from datetime import datetime
from urllib.parse import urlparse

from scrapy import Request
from scrapy.spiders import Spider

from mydm.ai import extract_tags
from mydm.items import ArticleItem
from mydm.spider.spider import ErrbackSpider


logger = logging.getLogger(__name__)
BLOGSPIDER_ATTRS = [
        'start_urls',
        'category',
        'entry_xpath',
        'item_title_xpath',
        'item_link_xpath',
        'item_content_xpath'
]


def set_item_tag(txt, item, encoding='utf-8'):
    tags = extract_tags(txt, encoding)
    if tags:
        item['tag'] = tags


class BLOGSpider(Spider):

    # must contained attribute
    ATTRS = ('title', 'link', 'content')

    def extract_entries(self, response):
        return response.selector.xpath(self.entry_xpath)

    def extract_item(self, entry, encoding):
        item = {
                attr: entry.xpath(xpath).extract_first()
                for attr, xpath in self.item_extractors
        }
        set_item_tag(
                entry.xpath('.').extract_first(),
                item,
                encoding
        )
        if item.get('link') is not None:
            item['link'] = item['link'].strip('\t\n\r ')
        if item.get('title') is not None:
            item['title'] = unescape(item['title'])
        return item

    def extract_content(self, response):
        item = response.meta['item']
        item['encoding'] = response.encoding
        item['link'] = response.url.strip('\t\n\r ')
        content = response.xpath(self.item_content_xpath).extract_first()
        item['content'] = content
        if item.get('tag') is None:
            set_item_tag(
                    content,
                    item,
                    response.encoding
            )
        if all(item.get(attr) is not None for attr in self.ATTRS):
            return ArticleItem(item)
        else:
            miss_attrs = [
                    attr
                    for attr in self.ATTRS
                    if item.get(attr) is None
            ]
            logger.error(
                    'spider[%s] extract content miss attrs%s',
                    self.name,
                    miss_attrs
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


class BLOGSpiderMeta(type):

    def __new__(cls, name, bases, attrs):
        if all(attr in attrs for attr in BLOGSPIDER_ATTRS):

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
                new_attrs['item_extractors'] = extractors
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
                    for attr in BLOGSPIDER_ATTRS
                    if attr not in attrs
            ]
            raise AttributeError(f'miss attributes{miss_attrs}')
