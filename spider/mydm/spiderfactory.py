# -*- coding: utf-8 -*-


from .spider import ErrbackSpider, SpiderMetaClses
from .exceptions import SpiderFactoryException


__all__ = [
        'SpiderFactory'
]


class SpiderFactory:
    """
        spider builder
    """
    @staticmethod
    def mkspider(setting):
        if 'name' not in setting or 'type' not in setting:
            raise SpiderFactoryException(
                'Error in SpiderFactory no name|type setting attribute found'
                )
        try:
            return SpiderMetaClses[setting['type']](
                    '{}Spider'.format(setting['name'].capitalize()),
                    (ErrbackSpider,),
                    setting)
        except KeyError:
            raise SpiderFactoryException((
                'Error in SpiderFactory type[{}] not support'
                ).format(setting['type']))
        except AttributeError as e:
            raise SpiderFactoryException('{}'.format(e))
