# -*- coding: utf-8 -*-


from mydm.exceptions import SpiderFactoryException
from mydm.spider import ErrbackSpider, SpiderMetaClses


__all__ = ['SpiderFactory']


class SpiderFactory:

    @staticmethod
    def mkspider(setting):
        if 'name' not in setting or 'type' not in setting:
            raise SpiderFactoryException(
                    'miss attribute[name|type]'
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
            raise SpiderFactoryException(f'build spider failed[{e}]')
