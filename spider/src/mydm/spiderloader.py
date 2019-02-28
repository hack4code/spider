# -*- coding: utf-8 -*-


import logging

from zope.interface import implementer
from scrapy.interfaces import ISpiderLoader

from mydm.util import cache_property
from mydm.model import get_spider_settings
from mydm.spiderfactory import SpiderFactory
from mydm.exceptions import SpiderFactoryException


__all__ = ['MongoSpiderLoader']


logger = logging.getLogger(__name__)


@implementer(ISpiderLoader)
class MongoSpiderLoader:

    @cache_property
    def spiders(self):
        spiders = {}
        for setting in get_spider_settings():
            spider_id = setting['_id']
            try:
                cls = SpiderFactory.create_spider(setting)
            except SpiderFactoryException as e:
                logger.error('spider create error[%s]', e)
            else:
                spiders[spider_id] = cls
        return spiders

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def load(self, spider_id):
        return self.spiders[spider_id]

    def find_by_request(self, request):
        return [
            spider_id
            for spider_id, cls in self.spiders.items()
            if cls.handles_request(request)
        ]

    def list(self):
        return list(self.spiders.keys())
