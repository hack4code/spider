# -*- coding: utf-8 -*-


try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
from collections import namedtuple

import redis

from scrapy.utils.project import get_project_settings

RedisConf = namedtuple('RedisUrl', ['host', 'port', 'database'])
settings = get_project_settings()


def parse_redis_url(url):
    parser = urlparse(url)
    host = parser.hostname
    port = parser.port
    db = int(parser.path[1:])
    return RedisConf(host, port, db)


def flush_failed_spider_db():
    conf = parse_redis_url(settings['RETRY_SPIDERS_URL'])
    r = redis.Redis(host=conf.host, port=conf.port, db=conf.database)
    r.flushdb()


def save_failed_spider(sp):
    conf = parse_redis_url(settings['RETRY_SPIDERS_URL'])
    r = redis.Redis(host=conf.host, port=conf.port, db=conf.database)
    r.rpush('spider', sp)


def get_failed_spiders():
    conf = parse_redis_url(settings['RETRY_SPIDERS_URL'])
    r = redis.Redis(host=conf.host, port=conf.port, db=conf.database)
    l = r.llen('spider')
    if l == 0:
        return []
    else:
        return r.lrange('spider', 0, l)
