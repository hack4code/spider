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

    @property
    def spiders(self):
        if self._spiders is None:
            spiders = {}
            for sp_setting in get_spider_settings():
                spid = sp_setting['_id']
                try:
                    spcls = mk_spider_cls(sp_setting)
                except SpiderFactoryException:
                    logger.exception((
                        'Error in SpiderFactory for spider[{}]'
                        ).format(spid))
                else:
                    spiders[spid] = spcls
            self._spiders = spiders
            logger.info('spiders count: {}'.format(len(spiders)))
        return self._spiders

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def load(self, spid):
        try:
            return self.spiders[spid]
        except KeyError:
            raise KeyError((
                'Error in loader, spider[{}] not found'
                ).format(spid))

    def find_by_request(self, request):
        return [name
                for name, cls in self.spiders.items()
                if cls.handles_request(request)]

    def list(self):
        return list(self.spiders.keys())
