# -*- coding: utf-8 -*-


from .mongodb import (
        get_spider_settings,
        save_article, save_spider_settings
)


__all__ = [
        'save_article',
        'get_spider_settings',
        'save_spider_settings'
]
