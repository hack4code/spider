# -*- coding: utf-8 -*-


from .log import logger
from .xml import mk_lxmlspider_cls
from .html import mk_blogspider_cls


class SpiderFactoryException(Exception):
    pass


spider_factory = {
    'xml': mk_lxmlspider_cls,
    'blog': mk_blogspider_cls
}


def mk_spider_cls(sp_setting):
    logger.info('create spider: {}'.format(sp_setting['name']))

    try:
        sptype = sp_setting['type']
    except KeyError:
        raise SpiderFactoryException('sp_setting no type found')

    try:
        factory = spider_factory[sptype]
    except KeyError:
        raise SpiderFactoryException('{} not supported'.format(sptype))

    try:
        return factory(sp_setting)
    except AttributeError:
        raise SpiderFactoryException('missing attribute')
