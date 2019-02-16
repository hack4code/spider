# -*- coding: utf-8 -*-


import redis

from mydm.util import parse_redis_url


class ETagMiddleware:

    def __init__(self, r):
        self.r = r

    @classmethod
    def from_crawler(cls, crawler):
        conf = parse_redis_url(crawler.settings['ETAG_URL'])
        r = redis.Redis(
                host=conf.host,
                port=conf.port,
                db=conf.database
        )
        return cls(r)

    def get_ETag(self, k):
        return self.r.get(k)

    def save_ETag(self, k, v):
        return self.r.set(k, v)

    def process_request(self, request, spider):
        etag = self.get_ETag(request.url)
        if etag is None:
            return
        request.headers.setdefault('If-None-Match', etag)

    def process_response(self, request, response, spider):
        if response.status != 200:
            return response
        if 'ETag' in response.headers and 'Content-Type' in response.headers:
            type = response.headers['Content-Type']
            if 'image' not in type:
                self.save_ETag(request.url, response.headers['ETag'])
        return response
