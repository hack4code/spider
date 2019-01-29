# -*- coding: utf-8 -*-


import logging
from urllib.parse import urlparse
from collections import namedtuple

import redis


logger = logging.getLogger(__name__)


def parse_redis_url(url):
    RedisConf = namedtuple('RedisUrl',
                           ['host', 'port', 'database'])
    parser = urlparse(url)
    host = parser.hostname
    port = parser.port
    db = int(parser.path[1:])
    return RedisConf(host, port, db)


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
        except redis.exceptions.ConnectionError:
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
        r.set(spid, value)
    except redis.exceptions.ConnectionError:
        logger.error('Error in save_stats failed to connect redis server')


class cache_property:

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        value = self.func(obj)
        setattr(obj, self.func.__name__, value)
        return value
