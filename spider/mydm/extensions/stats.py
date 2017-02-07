# -*- coding: utf-8 -*-


import logging

from redis.exceptions import ConnectionError
import redis

from scrapy import signals

from ..util import parse_redis_url


logger = logging.getLogger(__name__)


class ExtensionStats:
    def __init__(self, stats, settings):
        self.stats = stats
        self.redis_conf = parse_redis_url(settings['SPIDER_STATS_URL'])

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
        try:
            r = redis.Redis(host=self.conf.host,
                            port=self.conf.port,
                            db=self.conf.database)
            r.set(spider._id,
                  self.stats.get_value(spider._id))
        except ConnectionError:
            logger.error('Error in ExtensionStats connect redis server failed')

    def item_scraped(self, item, spider):
        self.stats.inc_value(spider._id)
