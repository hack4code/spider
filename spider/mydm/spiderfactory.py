# -*- coding: utf-8 -*-


import logging

from .spider import mk_lxmlspider_cls, mk_blogspider_cls


logger = logging.getLogger(__name__)


class SpiderFactoryException(Exception):
    """
        exception for spider factory
    """
    pass


class SpiderFactory(object):
    """
        spider builder
    """
    @staticmethod
    def make_spider(setting):
        _factory_func = {
            'xml': mk_lxmlspider_cls,
            'blog': mk_blogspider_cls
        }
        if 'name' not in setting or 'type' not in setting:
            raise SpiderFactoryException(
                'Error in SpiderFactory, no name|type attr found'
                )
        f = _factory_func.get(setting['type'])
        if f:
            return f(setting)
        else:
            raise SpiderFactoryException((
                'Error in SpiderFactory type[{}] not support'
                ).format(setting['type']))


def mk_spider_cls(setting):
    try:
        return SpiderFactory.make_spider(setting)
    except AttributeError:
        raise SpiderFactoryException('Error in mk_spider_cls attr')
    logger.info('Factory create spider[{}]'.format(setting['name']))
