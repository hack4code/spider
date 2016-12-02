# -*- coding: utf-8 -*-


import redis

from ..util import parse_redis_url


class StatsPipeline(object):
    def __init__(self, settings):
        conf = parse_redis_url(settings['SPIDER_STATS_URL'])
        self.r = redis.Redis(host=conf.host,
                             port=conf.port,
                             db=conf.database)

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def process_item(self, item, spider):
        self.r.incr(spider._id)
        return item
