# -*- coding: utf-8 -*-


from datetime import timedelta, datetime

from scrapy import signals


class IfModifySinceMiddleware:

    def __init__(self, delta=None):
        self.delta = delta

    @classmethod
    def from_crawler(cls, crawler):
        inst = cls(delta=crawler.settings['MODIFY_DELTA'])
        crawler.signals.connect(
                inst.spider_opened,
                signal=signals.spider_opened
        )
        return inst

    def spider_opened(self, spider):
        self.delta = getattr(
                spider,
                'modify_delta',
                self.delta
        )

    def process_request(self, request, spider):
        if not self.delta:
            return
        last = datetime.utcnow() - timedelta(days=self.delta)
        request.headers.setdefault(
            'If-Modified-Since',
            last.strftime('%a, %d %b %Y %H:%M:%S GMT')
        )
