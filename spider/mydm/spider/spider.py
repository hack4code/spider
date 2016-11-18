# -*- coding: utf-8 -*-


from twisted.internet.error import TimeoutError

from scrapy.spiders import Spider
from scrapy import Request

from ..log import logger
from ..util import save_failed_spider


class ErrbackSpider(Spider):

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,
                          callback=self.parse,
                          errback=self.errback)

    def errback(self, failure):
        if failure.check(TimeoutError):
            request = failure.request
            logger.error('TimeoutError on {}'.format(request))
        else:
            logger.error(repr(failure))
        save_failed_spider(self._id)
