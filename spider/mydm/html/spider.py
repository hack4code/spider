# -*- coding: utf-8 -*-


try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
from datetime import datetime
import inspect

from scrapy.selector import Selector
from scrapy import Request

from ..spider import ErrbackSpider
from ..log import logger
from ..items import ArticleItem
from ..ai import TagExtractor


class BLOGSpiderException(Exception):
    pass


class BLOGSpider(ErrbackSpider):
    """
    tags item must contain
    """
    TAGS = ('title', 'link', 'content')

    def check_item(self, item):
        return True if all(tag in item and item[tag] is not None
                           for tag in self.TAGS) else False

    def extract_entries(self, response):
        return Selector(response, type='html').xpath(self.entry_xpath)

    def extract_item(self, entry):
        attrs = inspect.getmembers(self.__class__,
                                   lambda a: not(inspect.isroutine(a)))
        extractors = [attr for attr in attrs
                      if attr[0].startswith('item_') and
                      attr[0].endswith('_xpath') and
                      attr[0] != 'item_content_xpath']
        item = {name.split('_')[1]: entry.xpath(xnode).extract_first()
                for name, xnode in extractors}
        tags = TagExtractor()(entry.xpath('.').extract_first())
        if tags is not None:
            item['tag'] = tags

        def clean_link_url(url):
            return url.strip('\t\n\r\s')

        if 'link' in item and item['link'] is not None:
            item['link'] = clean_link_url(item['link'])

        if 'title' in item and item['title'] is not None:
            from html import unescape
            item['title'] = unescape(item['title'])

        return item

    def extract_content(self, response):
        item = response.meta['item']
        tags = TagExtractor()(response.text)
        if tags is not None:
            item['tag'] = tags
        item['encoding'] = response.encoding
        item['link'] = response.url
        content = response.xpath(self.item_content_xpath).extract_first()
        item['content'] = content
        if self.check_item(item):
            return ArticleItem(item)
        else:
            miss_tags = [tag for tag in self.TAGS
                         if tag not in item or item[tag] is None]
            logger.error(('Error in spider {} extract content, '
                         'miss tags[{}]').format(self.name,
                                                 miss_tags))

    def parse(self, response):
        try:
            prelink = response.xpath(self.link_pre_xpath).extract_first()
            yield Request(prelink,
                          callback=self.parse,
                          errback=self.errback)
        except AttributeError:
            logger.info('{} has no prelink attr'.format(self.name))

        for entry in self.extract_entries(response):
            item = self.extract_item(entry)
            item['category'] = self.category
            item['crawl_date'] = datetime.now()
            item['domain'] = urlparse(response.request.url).netloc
            item['data_type'] = 'html'
            link = item['link']
            if link is None:
                continue
            link = link.strip()
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
            return super(BLOGSpiderMeta, cls).__new__(cls, name, bases, attrs)
        else:
            raise AttributeError


def mk_blogspider_cls(sp_setting):
    return BLOGSpiderMeta('{}Spider'.format(sp_setting['name']),
                          (BLOGSpider,),
                          sp_setting)
