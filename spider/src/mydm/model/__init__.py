# -*- coding: utf-8 -*-


from .mongodb import (
        is_exists_feed, save_feed, is_exists_article,
        is_exists_spider,
        save_article, save_spider_settings,
        get_spider_settings, get_category_tags,
        log_spider_scrape_count,
)

from .redis import get_stats, save_stats


__all__ = [
        'is_exists_feed',
        'is_exists_article',
        'is_exists_spider',
        'get_spider_settings',
        'get_category_tags',
        'save_feed',
        'save_article',
        'save_spider_settings',
        'log_spider_scrape_count',
        'save_stats',
        'get_stats',
]
