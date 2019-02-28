# -*- coding: utf-8 -*-


import importlib
from pathlib import Path


def register_meta_classes():
    path = Path(__file__).parent
    for item in path.iterdir():
        if not item.is_dir():
            continue
        spider_path = item / 'spider.py'
        if not spider_path.exists():
            continue
        spider_module = f'.{item.absolute().name}.spider'
        importlib.import_module(spider_module, __package__)
