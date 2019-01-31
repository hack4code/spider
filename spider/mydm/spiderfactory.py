# -*- coding: utf-8 -*-


from mydm.spider import ErrbackSpider, SpiderMetaClses
from mydm.exceptions import SpiderFactoryException


__all__ = ['SpiderFactory']


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
            build = SpiderMetaClses[setting['type']]
        except KeyError:
            raise SpiderFactoryException((
                f'Error in SpiderFactory type[{setting["type"]}] not support'
                ).format())
        try:
            return build(
                    f'{setting["name"].capitalize()}Spider',
                    (ErrbackSpider, ),
                    setting
            )
        except AttributeError as e:
            raise SpiderFactoryException(f'{e}')
