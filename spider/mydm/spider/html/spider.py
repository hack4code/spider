# -*- coding: utf-8 -*-


import logging
from urllib.parse import urlparse
from datetime import datetime
import inspect
from html import unescape

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request

from ..spider import ErrbackSpider
from ...items import ArticleItem
from ...ai import TagExtractor


logger = logging.getLogger(__name__)


class BLOGSpiderException(Exception):
    """
        Exception for blog spider
    """
    pass


def extract_tags(doc, encoding):
    extract = TagExtractor()
    return extract(doc, encoding=encoding)


class BLOGSpider(Spider):
    """
        spider crawl blog with xpath
    """

    # must contain
    ATTRS = ('title',
             'link',
             'content')

    def check_item(self, item):
        return True if all(_ in item and item[_] is not None
                           for _ in self.ATTRS) else False

    def extract_entries(self, response):
        return Selector(response,
                        type='html'
                        ).xpath(self.entry_xpath)

    def extract_item(self, entry, encoding):
        # extract item
        attrs = inspect.getmembers(self.__class__,
                                   lambda a: not(inspect.isroutine(a)))
        extractors = [_ for _ in attrs
                      if _[0].startswith('item_') and
                      _[0].endswith('_xpath') and
                      _[0] != 'item_content_xpath']
        item = {name.split('_')[1]: entry.xpath(xnode).extract_first()
                for name, xnode in extractors}
        # extract tag
        tags = extract_tags(entry.xpath('.').extract_first(),
                            encoding)
        if tags is not None:
            item['tag'] = tags
        # strip link
        if 'link' in item and item['link'] is not None:
            item['link'] = item['link'].strip('\t\n\r\s')
        # unescape title
        if 'title' in item and item['title'] is not None:
            item['title'] = unescape(item['title'])
        return item

    def extract_content(self, response):
        item = response.meta['item']
        item['encoding'] = response.encoding
        item['link'] = response.url
        content = response.xpath(self.item_content_xpath).extract_first()
        item['content'] = content
        if 'tag' not in item:
            tags = extract_tags(content,
                                response.encoding)
            if tags is not None:
                item['tag'] = tags
        if self.check_item(item):
            return ArticleItem(item)
        else:
            miss_attrs = [_ for _ in self.ATTRS
                          if _ not in item or item[_] is None]
            logger.error((
                'Error in spider {} extract content, miss attrs{}'
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
        if all(attr in attrs for attr in ATTRS):
            return super(BLOGSpiderMeta,
                         cls).__new__(cls,
                                      name,
                                      bases,
                                      attrs)
        else:
            raise AttributeError


def mk_blogspider_cls(setting):
    return BLOGSpiderMeta('{}Spider'.format(setting['name'].capitalize()),
                          (BLOGSpider, ErrbackSpider),
                          setting)
