# -*- coding: utf-8 -*-


from mydm.exceptions import SpiderFactoryException
from mydm.spider import ErrbackSpider, SpiderMetaClses


__all__ = ['SpiderFactory']


class SpiderFactory:
    """
        spider builder
    """
    @staticmethod
    def mkspider(setting):
        if 'name' not in setting or 'type' not in setting:
            raise SpiderFactoryException(
                    'no name|type setting attribute found'
            )
        try:
            build = SpiderMetaClses[setting['type']]
        except KeyError:
            raise SpiderFactoryException(
                    f'unknown spider type[{setting["type"]}]'
            )
        try:
            return build(
                    f'{setting["name"].capitalize()}Spider',
                    (ErrbackSpider, ),
                    setting
            )
        except AttributeError as e:
            raise SpiderFactoryException(f'build spider failed{e}')
