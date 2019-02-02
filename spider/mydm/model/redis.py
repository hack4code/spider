# -*- coding: utf-8 -*-


import logging

import redis

from scrapy.utils.project import get_project_settings

from mydm.util import parse_redis_url


SETTINGS = get_project_settings()


logger = logging.getLogger(__name__)


def get_stats(spids):
    stats = {}
    conf = parse_redis_url(SETTINGS['TEMP_SPIDER_STATS_URL'])
    r = redis.Redis(
            host=conf.host,
            port=conf.port,
            db=conf.database
    )
    for spid in spids:
        n = None
        try:
            n = r.get(spid)
            r.delete(spid)
        except redis.exceptions.ConnectionError:
            logger.error('get_stats failed to connect redis server')
        n = 0 if n is None else int(n)
        stats[spid] = n
    return stats


def save_stats(spider, value):
    spid = str(spider._id)
    conf = parse_redis_url(SETTINGS['TEMP_SPIDER_STATS_URL'])
    r = redis.Redis(
            host=conf.host,
            port=conf.port,
            db=conf.database
    )
    try:
        r.set(spid, value)
    except redis.exceptions.ConnectionError:
        logger.error('save_stats failed to connect redis server')
