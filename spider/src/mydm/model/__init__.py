# -*- coding: utf-8 -*-


from .mongodb import (
        is_exists_feed, is_exists_article,
        save_feed, save_article, save_spider_settings,
        get_spider_settings
)


__all__ = [
        'is_exists_feed',
        'is_exists_article',
        'get_spider_settings',
        'save_feed',
        'save_article',
        'save_spider_settings',
]
