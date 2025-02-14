# -*- coding: utf-8 -*-


import importlib
from pathlib import Path


__all__ = [
    'register_spider_meta_cls',
    'create_spider_class_from_setting',
    'SpiderFactoryException',
]


SPIDER_META_CLSES = {}


class SpiderFactoryException(Exception):
    pass


def register_spider_meta_cls(tyep, klass):
    SPIDER_META_CLSES[tyep] = klass


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


def create_spider_class_from_setting(setting):
    if not all(attr in setting for attr in ('name', 'type', 'title')):
        raise SpiderFactoryException(
                'miss attribute[name|type|title]'
        )
    if not SPIDER_META_CLSES:
        import_spiders()
    try:
        metacls = SPIDER_META_CLSES[setting['type']]
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
