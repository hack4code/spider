# -*- coding: utf-8 -*-


import logging
from urllib.parse import urlparse
from datetime import datetime
from html import unescape

from scrapy.spiders import Spider
from scrapy import Request

from mydm.items import ArticleItem
from mydm.ai import extract_tags
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
    """
        blog spider crawling with xpath
    """

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
        if all(_ in attrs for _ in BLOGSPIDER_ATTRS):
            def update_bases(bases):
                assert BLOGSpider not in bases, 'BLOGSpider in bases'
                bases_ = [BLOGSpider]
                bases_.extend(bases)
                if ErrbackSpider not in bases_:
                    bases_.append(ErrbackSpider)
                return tuple(bases_)

            def update_attrs(attrs):
                attrs_ = attrs.copy()
                extractors = []
                for k, v in attrs_.items():
                    fields = k.split('_')
                    if (len(fields) == 3 and fields[0] == 'item' and
                            fields[1] != 'content' and fields[2] == 'xpath'):
                        extractors.append((fields[1], v))
                attrs_['item_extractors'] = extractors
                for k, _ in extractors:
                    del attrs_['item_{}_xpath'.format(k)]
                return attrs_

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
