# -*- coding: utf-8 -*-


from .spider import mk_lxmlspider_cls, mk_blogspider_cls
from .log import logger


class SpiderFactoryException(Exception):
    """
        exception for factory make spider
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
        if 'name' not in setting:
            raise SpiderFactoryException((
                'Error in SpiderFactory, no name attr found'
                ))
        t = setting['type']
        try:
            return _factory_func[t](setting)
        except KeyError:
            raise SpiderFactoryException((
                'Error in SpiderFactory, {} type not support'
                ).format(t))


def mk_spider_cls(setting):
    logger.info('Factory create spider[{}]'.format(setting['name']))
    try:
        return SpiderFactory.make_spider(setting)
    except AttributeError:
        raise SpiderFactoryException('Error in mk_spider_cls, attr error')
