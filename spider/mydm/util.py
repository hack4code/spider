# -*- coding: utf-8 -*-


try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
from collections import namedtuple


RedisConf = namedtuple('RedisUrl', ['host', 'port', 'database'])


def parse_redis_url(url):
    parser = urlparse(url)
    host = parser.hostname
    port = parser.port
    db = int(parser.path[1:])
    return RedisConf(host, port, db)
