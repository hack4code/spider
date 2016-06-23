# -*- coding: utf-8 -*-


import redis

from ..util import parse_redis_url


class CountPipeline(object):
    def __init__(self, settings):
        conf = parse_redis_url(settings['STATS_URL'])
        self.r = redis.Redis(host=conf.host, port=conf.port, db=conf.database)
        self.key = settings['STATS_KEY']
        self.r.set(self.key, 0)

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def process_item(self, item, spider):
        self.r.incr(self.key)
        return item
