# -*- coding: utf-8 -*-


import logging
from zope.interface import implementer
from scrapy.interfaces import ISpiderLoader

from .spiderfactory import mk_spider_cls, SpiderFactoryException
from .model import get_spider_settings


logger = logging.getLogger(__name__)


@implementer(ISpiderLoader)
class MongoSpiderLoader(object):
    def __init__(self):
        self._spiders = None

    def _load_spiders(self):
        spiders = {}
        for sp_setting in get_spider_settings():
            spid = str(sp_setting['_id'])
            try:
                spcls = mk_spider_cls(sp_setting)
            except SpiderFactoryException:
                logger.error('spider({}) class create error'.format(spid))
            else:
                spiders[spid] = spcls
        self._spiders = spiders

    @property
    def spiders(self):
        if self._spiders is None:
            self._load_spiders()
        return self._spiders

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def load(self, spid):
        try:
            return self.spiders[spid]
        except KeyError:
            raise KeyError('spider({}) not found'.format(spid))

    def find_by_request(self, request):
        return [name
                for name, cls in self.spiders.items()
                if cls.handles_request(request)]

    def list(self):
        return list(self.spiders.keys())
