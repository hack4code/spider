# -*- coding: utf-8 -*-


import logging

from zope.interface import implementer
from scrapy.interfaces import ISpiderLoader

from mydm.model import get_spider_settings
import mydm.spiderfactory as factory


__all__ = ['MongoSpiderLoader']


logger = logging.getLogger(__name__)


@implementer(ISpiderLoader)
class MongoSpiderLoader:
    @property
    def spiders(self):
        if hasattr(self, '_spiders'):
            return self._spiders
        spiders = {}
        for setting in get_spider_settings():
            spider_id = setting['_id']
            try:
                cls = factory.create_spider_class_from_setting(setting)
            except Exception:
                logger.exception('create_spider_class_from_setting failed:')
            else:
                spiders[spider_id] = cls
        self._spiders = spiders
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
