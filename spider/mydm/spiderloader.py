# -*- coding: utf-8 -*-


import logging

from zope.interface import implementer

from scrapy.interfaces import ISpiderLoader

from .spiderfactory import SpiderFactory, SpiderFactoryException
from .model import get_spider_settings


logger = logging.getLogger(__name__)


@implementer(ISpiderLoader)
class MongoSpiderLoader:
    def __init__(self):
        self._spiders = None

    @property
    def spiders(self):
        if self._spiders is None:
            spiders = {}
            for setting in get_spider_settings():
                spid = setting['_id']
                try:
                    cls = SpiderFactory.mkspider(setting)
                except SpiderFactoryException as e:
                    logger.error('{}'.format(e))
                else:
                    spiders[spid] = cls
            self._spiders = spiders
        return self._spiders

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
