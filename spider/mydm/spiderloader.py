# -*- coding: utf-8 -*-


import logging

from zope.interface import implementer

from scrapy.interfaces import ISpiderLoader

from .exceptions import SpiderFactoryException
from .spiderfactory import SpiderFactory
from .model import get_spider_settings
from .util import cache_porperty


__all__ = [
        'MongoSpiderLoader'
]


logger = logging.getLogger(__name__)


@implementer(ISpiderLoader)
class MongoSpiderLoader:

    @cache_porperty
    def spiders(self):
        spiders = {}
        for setting in get_spider_settings():
            spid = setting['_id']
            try:
                cls = SpiderFactory.mkspider(setting)
            except SpiderFactoryException as e:
                logger.error(
                        'MongoSpiderLoader got SpiderFactoryException[{}]',
                        e)
            else:
                spiders[spid] = cls
        return spiders

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def load(self, spid):
        return self.spiders[spid]

    def find_by_request(self, request):
        return [spid for spid, cls in self.spiders.items()
                if cls.handles_request(request)]

    def list(self):
        return list(self.spiders.keys())
