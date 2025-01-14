# -*- coding: utf-8 -*-


import importlib
from pathlib import Path

from mydm.spider import SpiderMeta
from mydm.exceptions import SpiderFactoryException


__all__ = ['SpiderFactory']


def import_spiders():
    path = Path(__file__).parent / 'spider/'
    for item in path.iterdir():
        if not item.is_dir():
            continue
        spider_path = item / 'spider.py'
        if not spider_path.exists():
            continue
        spider_module = f'.spider.{item.absolute().name}.spider'
        importlib.import_module(spider_module, __package__)


class SpiderFactory:
    @classmethod
    def from_setting(cls, setting):
        if not all(attr in setting for attr in ('name', 'type', 'title')):
            raise SpiderFactoryException(
                    'miss attribute[name|type]'
            )
        if not SpiderMeta.CLS:
            import_spiders()
        try:
            metacls = SpiderMeta.CLS[setting['type']]
        except KeyError:
            raise SpiderFactoryException(
                    f'unknown spider type[{setting["type"]}]'
            )
        try:
            return metacls(
                    f'{setting["name"].capitalize()}Spider',
                    (),
                    setting
            )
        except AttributeError as e:
            raise SpiderFactoryException(f'build spider failed[{e}]')
