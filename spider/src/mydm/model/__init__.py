# -*- coding: utf-8 -*-


from .mongodb import (
        is_exists_feed, is_exists_article, is_exists_spider,
        save_feed, save_article, save_spider_settings,
        get_spider_settings, get_category_tags,
)


__all__ = [
        'is_exists_feed',
        'is_exists_article',
        'is_exists_spider',
        'get_spider_settings',
        'get_category_tags',
        'save_feed',
        'save_article',
        'save_spider_settings',
]
