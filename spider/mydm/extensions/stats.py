# -*- coding: utf-8 -*-


import logging

from scrapy import signals

from ..util import save_stats


logger = logging.getLogger(__name__)


class ExtensionStats:
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.stats)
        crawler.signals.connect(
                ext.spider_opened,
                signal=signals.spider_opened
        )
        crawler.signals.connect(
                ext.spider_closed,
                signal=signals.spider_closed
        )
        crawler.signals.connect(
                ext.item_scraped,
                signal=signals.item_scraped
        )
        return ext

    def spider_opened(self, spider):
        pass

    def item_scraped(self, item, spider):
        pass

    def spider_closed(self, spider):
        item_scraped_count = self.stats.get_value('item_scraped_count', 0)
        save_stats(
                spider.settings['SPIDER_STATS_URL'],
                spider._id,
                item_scraped_count
        )
        if spider.settings['BOT_NAME'] == 'TestSpider':
            return
        logger.info(
                'spider[%s] crawled %d articles',
                spider.name,
                item_scraped_count
        )
