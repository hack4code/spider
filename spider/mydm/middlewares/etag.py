# -*- coding: utf-8 -*-


import logging
import redis

from ..util import parse_redis_url


logger = logging.getLogger(__name__)


class ETagMiddleware(object):
    def __init__(self, settings):
        conf = parse_redis_url(settings['ETAG_URL'])
        self.r = redis.Redis(host=conf.host, port=conf.port, db=conf.database)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def get_ETag(self, k):
        return self.r.get(k)

    def save_ETag(self, k, v):
        return self.r.set(k, v)

    def process_request(self, request, spider):
        etag = self.get_ETag(request.url)
        if etag is not None:
            request.headers.setdefault('If-None-Match', etag)
        return None

    def process_response(self, request, response, spider):
        if response.status != 200:
            return response
        if 'ETag' in response.headers and 'Content-Type' in response.headers:
            ct = response.headers['Content-Type']
            if 'image' not in ct:
                self.save_ETag(request.url, response.headers['ETag'])
        return response
