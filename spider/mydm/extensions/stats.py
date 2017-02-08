# -*- coding: utf-8 -*-


import logging

from scrapy import signals

from ..util import save_stats
from ..model import update_spider_stats


logger = logging.getLogger(__name__)


class ExtensionStats:
    def __init__(self, stats, settings):
        self.stats = stats
        self.url = settings['SPIDER_STATS_URL']

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.stats,
                  crawler.settings)
        crawler.signals.connect(ext.spider_opened,
                                signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed,
                                signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped,
                                signal=signals.item_scraped)

        return ext

    def spider_opened(self, spider):
        self.stats.set_value(spider._id,
                             0)

    def spider_closed(self, spider):
        value = self.stats.get_value(spider._id)
        save_stats(self.url,
                   spider._id,
                   value)
        logger.info('spider[%s] crawled %d articles',
                    spider.name,
                    value)
        if value == 0:
            update_spider_stats(spider,
                                {'fail': 1})

    def item_scraped(self, item, spider):
        self.stats.inc_value(spider._id)
