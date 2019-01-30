# -*- coding: utf-8 -*-


import logging
from urllib.parse import urlparse

from scrapy.spiders import Spider
from scrapy import Request

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


logger = logging.getLogger(__name__)


class ErrbackSpider(Spider):

    def start_requests(self):
        for _ in self.start_urls:
            logger.info('request for %s', _)
            yield Request(_,
                          callback=self.parse,
                          errback=self.errback,
                          dont_filter=True)

    def errback(self, failure):
        if failure.check(DNSLookupError):
            host = urlparse(failure.request.url).hostname
            logger.error('DNSLookupError on host[%s]', host)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            logger.error('TimeoutError on url[%s]', request.url)
        elif failure.check(HttpError):
            response = failure.value.response
            logger.error('HttpError on url[%s, status=%d]',
                         response.url,
                         response.status)
        else:
            logger.error('SpiderError on url[%s, error=%s',
                         failure.request.url,
                         repr(failure))
