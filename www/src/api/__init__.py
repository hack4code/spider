# -*- coding: utf-8 -*-


from flask import Blueprint
from flask_restful import Api

from .feed import CrawlArticles, RssFeed, BlogFeed
from .db import Day, Entries, Spiders


__all__ = ['init_api']


def init_api(app):
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)
    api.add_resource(Day, '/api/day')
    api.add_resource(Entries, '/api/entries')
    api.add_resource(Spiders, '/api/spiders')
    api.add_resource(CrawlArticles, '/submit/crawl')
    api.add_resource(RssFeed, '/submit/rss')
    api.add_resource(BlogFeed, '/submit/blog')
    app.register_blueprint(api_bp)
