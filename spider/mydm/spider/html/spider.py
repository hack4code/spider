# -*- coding: utf-8 -*-


import logging
from urllib.parse import urlparse
from datetime import datetime
from html import unescape

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request

from ..spider import ErrbackSpider
from ...items import ArticleItem
from ...ai import extract_tags


logger = logging.getLogger(__name__)

BLOGSPIDER_ATTRS = ['start_urls',
                    'category',
                    'entry_xpath',
                    'item_title_xpath',
                    'item_link_xpath',
                    'item_content_xpath']


class BLOGSpider(Spider):
    """
        blog spider crawling with xpath
    """

    # article item must contained attribute
    ATTRS = ('title', 'link', 'content')

    def extract_entries(self, response):
        return Selector(response,
                        type='html'
                        ).xpath(self.entry_xpath)

    def extract_item(self, entry, encoding):
        item = {attr: entry.xpath(xpath).extract_first()
                for attr, xpath in self.item_extractors}
        tags = extract_tags(entry.xpath('.').extract_first(),
                            encoding)
        if tags:
            item['tag'] = tags
        if item.get('link') is not None:
            item['link'] = item['link'].strip('\t\n\r\s')
        if item.get('title') is not None:
            item['title'] = unescape(item['title'])
        return item

    def extract_content(self, response):
        item = response.meta['item']
        item['encoding'] = response.encoding
        item['link'] = response.url
        content = response.xpath(self.item_content_xpath).extract_first()
        item['content'] = content
        if item.get('tag') is None:
            tags = extract_tags(content,
                                response.encoding)
            if tags:
                item['tag'] = tags
        if all(item.get(_) is not None for _ in self.ATTRS):
            return ArticleItem(item)
        else:
            miss_attrs = [_ for _ in self.ATTRS if item.get(_) is None]
            logger.error('Error in spider %s extract content miss attrs%s',
                         self.name,
                         miss_attrs)

    def parse(self, response):
        try:
            xplink = self.link_pre_xpath
        except AttributeError:
            pass
        else:
            prelink = response.xpath(xplink).extract_first()
            yield Request(prelink,
                          callback=self.parse,
                          errback=self.errback)

        for entry in self.extract_entries(response):
            item = self.extract_item(entry,
                                     response.encoding)
            item['category'] = self.category
            item['crawl_date'] = datetime.now()
            item['domain'] = urlparse(response.request.url).netloc
            item['data_type'] = 'html'
            link = item.get('link')
            if link is None:
                continue
            link = link.strip('\r\n\s\t')
            if not link.startswith('http'):
                item['link'] = response.urljoin(link)
            yield Request(item['link'],
                          meta={'item': item},
                          callback=self.extract_content,
                          errback=self.errback,
                          dont_filter=True)


class BLOGSpiderMeta(type):
    def __new__(cls, name, bases, attrs):
        if all(_ in attrs for _ in BLOGSPIDER_ATTRS):
            def update_bases(bases):
                assert BLOGSpider not in bases, "BLOGSpider in bases"
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

            return super().__new__(cls,
                                   name,
                                   update_bases(bases),
                                   update_attrs(attrs))
        else:
            miss_attrs = [_ for _ in BLOGSPIDER_ATTRS if _ not in attrs]
            raise AttributeError((
                'Error in BLOGSpiderMeta miss attributes{}'
                ).format(miss_attrs))
