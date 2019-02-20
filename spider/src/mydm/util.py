# -*- coding: utf-8 -*-


from urllib.parse import urlparse
from collections import namedtuple


RedisConf = namedtuple('RedisUrl', ['host', 'port', 'database'])


def parse_redis_url(url):
    parser = urlparse(url)
    host = parser.hostname
    port = parser.port
    db = int(parser.path[1:])
    return RedisConf(host, port, db)


class cache_property:

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        value = self.func(obj)
        setattr(obj, self.func.__name__, value)
        return value
