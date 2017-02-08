# -*- coding: utf-8 -*-


from urllib.parse import urlparse

from scrapy.spiders import Spider
from scrapy import Request
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class ErrbackSpider(Spider):

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,
                          callback=self.parse,
                          errback=self.errback)

    def errback(self, failure):
        if failure.check(DNSLookupError):
            host = urlparse(failure.request.url).hostname
            self.logger.error('DNSLookupError on domain[%s]',
                              host)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on url[%s]',
                              request.url)
        elif failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on url[%s, code=%d]',
                              response.url,
                              response.code)
        else:
            self.logger.error(repr(failure))
