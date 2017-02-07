# -*- coding: utf-8 -*-


import logging
from urllib.parse import urlparse
from datetime import datetime
import inspect
from html import unescape

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request

from ...items import ArticleItem
from ...ai import extract_tags


logger = logging.getLogger(__name__)


class BLOGSpider(Spider):
    """
        blog spider crawling with xpath
    """

    # must contain
    ATTRS = ('title',
             'link',
             'content')

    @property
    def item_extractors(self):
        if not hasattr(self,
                       '_item_extractors'):
            extractors = []
            attrs = inspect.getmembers(self.__class__,
                                       lambda _: not(inspect.isroutine(_)))
            for k, v in attrs:
                fields = k.split('_')
                if (len(fields) == 3 and fields[0] == 'item' and
                        fields[1] != 'content' and fields[2] == 'xpath'):
                    extractors.append((fields[1], v))
            self._item_extractors = extractors
        return self._item_extractors

    def extract_entries(self, response):
        return Selector(response,
                        type='html'
                        ).xpath(self.entry_xpath)

    def extract_item(self, entry, encoding):
        item = {k: entry.xpath(v).extract_first()
                for k, v in self.item_extractors}
        # extract tag
        tags = extract_tags(entry.xpath('.').extract_first(),
                            encoding)
        if tags is not None:
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
            if tags is not None:
                item['tag'] = tags
        if all(item.get(_) is not None for _ in self.ATTRS):
            return ArticleItem(item)
        else:
            miss_attrs = [_ for _ in self.ATTRS if item.get(_) is None]
            logger.error((
                'Error in spider {} extract content miss attrs{}'
                ).format(self.name,
                         miss_attrs))

    def parse(self, response):
        try:
            prelink = response.xpath(self.link_pre_xpath).extract_first()
            yield Request(prelink,
                          callback=self.parse,
                          errback=self.errback)
        except AttributeError:
            logger.info('{} has no prelink attribute'.format(self.name))

        for entry in self.extract_entries(response):
            item = self.extract_item(entry,
                                     response.encoding)
            item['category'] = self.category
            item['crawl_date'] = datetime.now()
            item['domain'] = urlparse(response.request.url).netloc
            item['data_type'] = 'html'
            link = item['link']
            if link is None:
                continue
            link = link.strip('\r\n\s\t')
            if not link.startswith('http'):
                item['link'] = response.urljoin(link)
            yield Request(item['link'],
                          callback=self.extract_content,
                          errback=self.errback,
                          meta={'item': item})


class BLOGSpiderMeta(type):
    def __new__(cls, name, bases, attrs):
        ATTRS = ['start_urls',
                 'category',
                 'item_title_xpath',
                 'item_link_xpath',
                 'item_content_xpath']
        if all(_ in attrs for _ in ATTRS):
            bases_ = [_ for _ in bases if issubclass(_,
                                                     Spider)]
            if BLOGSpider not in bases_:
                bases_.append(BLOGSpider)
            bases_.extend([_ for _ in bases if not issubclass(_,
                                                              Spider)])
            return super().__new__(cls,
                                   name,
                                   tuple(bases_),
                                   attrs)
        else:
            miss_attrs = [_ for _ in ATTRS if _ not in attrs]
            raise AttributeError((
                'Error in BLOGSpiderMeta miss attributes{}'
                ).format(miss_attrs))
