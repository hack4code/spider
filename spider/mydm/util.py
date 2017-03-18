# -*- coding: utf-8 -*-


import logging
from urllib.parse import urlparse
from collections import namedtuple

import redis
from redis.exceptions import ConnectionError


logger = logging.getLogger(__name__)


def parse_redis_url(url):
    RedisConf = namedtuple('RedisUrl',
                           ['host', 'port', 'database'])
    parser = urlparse(url)
    host = parser.hostname
    port = parser.port
    db = int(parser.path[1:])
    return RedisConf(host,
                     port,
                     db)


def get_stats(url, spids):
    stats = {}
    conf = parse_redis_url(url)
    r = redis.Redis(host=conf.host,
                    port=conf.port,
                    db=conf.database)
    for spid in spids:
        n = None
        try:
            n = r.get(spid)
            r.delete(spid)
        except ConnectionError:
            logger.error('Error in get_stats failed to connect redis server')
        n = 0 if n is None else int(n)
        stats[spid] = n
    return stats


def save_stats(url, spid, value):
    conf = parse_redis_url(url)
    r = redis.Redis(host=conf.host,
                    port=conf.port,
                    db=conf.database)
    try:
        r.set(spid,
              value)
    except ConnectionError:
        logger.error('Error in save_stats failed to connect redis server')


class cache_porperty:

    def __init__(self, func):
        self.__name__ = func.__name__
        self.func = func

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__,
                                 None)
        if value is None:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
            return value
