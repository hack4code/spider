# -*- coding: utf-8 -*-


import grpc
from flask import request, current_app

from marshmallow import (
        Schema, fields, validates, pre_load, ValidationError
)
from flask_restful import Resource

import spider_pb2
import spider_pb2_grpc


def create_grpc_stub():
    channel = grpc.insecure_channel(current_app.config['GRPC_HOST'])
    stub = spider_pb2_grpc.SpiderRpcStub(channel)
    return stub


class StripSchema(Schema):

    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)

    @pre_load
    def strip(self, data):
        new_data = {}
        for key, val in data.items():
            if isinstance(val, str):
                val = val.strip(' \r\t\n')
            elif isinstance(val, (list, tuple)):
                val = list(
                        filter(
                            lambda _: _,
                            (item.strip(' \r\t\n') for item in val)
                        )
                )
            if val:
                new_data[key] = val
        return new_data


class CrawlArticles(Resource):

    def post(self):

        class SpiderListSchema(StripSchema):
            spiders = fields.List(fields.String())

        schema = SpiderListSchema()
        try:
            spiders = schema.load(request.get_json()).data
        except Exception:
            return {'message': 'invalid spiders'}, 400
        if not spiders:
            return {'message': 'no spider found'}, 400
        current_app.logger.info(f'spiders for crawl [{spiders}]')
        splist = spider_pb2.SpiderList()
        splist.spider.extend(spiders['spiders'])
        stub = create_grpc_stub()
        try:
            stub.CrawlArticles(splist)
        except Exception as e:
            return {'message': f'unknow error[{e}]'}, 400
        return '', 200


class FeedSchema(StripSchema):

    @validates('category')
    def validate_category(self, category):
        if category not in current_app.config['ARTICLE_CATEGORIES']:
            raise ValidationError(f'category value {category} is invalid')


class RssFeed(Resource):

    def post(self):

        class AtomFeedSchema(FeedSchema):
            url = fields.Url(required=True)
            category = fields.String(required=True)
            item_content_xpath = fields.String()
            removed_xpath_nodes = fields.List(fields.String())

        schema = AtomFeedSchema()
        try:
            feed = schema.load(request.get_json()).data
        except ValidationError as err:
            return {'message': err.messages}, 400
        except Exception:
            return {'message': 'invalid atom feed'}, 400
        current_app.logger.info(f'atom feed[{feed}]')
        if 'removed_xpath_nodes' in feed:
            nodes = feed.pop('removed_xpath_nodes')
        else:
            nodes = None
        rss_feed = spider_pb2.RssFeed(**feed)
        if nodes:
            rss_feed.removed_xpath_nodes.extend(nodes)
        stub = create_grpc_stub()
        try:
            result = stub.SubmitRssFeed(rss_feed)
        except Exception as e:
            return {'message': f'unknow error[{e}]'}, 400
        if result.error:
            return {'message': result.message}, 400
        else:
            return '', 200


class BlogFeed(Resource):

    def post(self):

        class BlogFeedSchema(FeedSchema):
            url = fields.Url(required=True)
            category = fields.String(required=True)
            entry_xpath = fields.String(required=True)
            item_title_xpath = fields.String(required=True)
            item_link_xpath = fields.String(required=True)
            item_content_xpath = fields.String(required=True)
            removed_xpath_nodes = fields.List(fields.String())

        schema = BlogFeedSchema()
        try:
            feed = schema.load(request.get_json()).data
        except ValidationError as err:
            return {'message': err.messages}, 400
        except Exception:
            return {'message': 'invalid blog feed'}, 400
        current_app.logger.info(f'blog feed[{feed}]')
        if 'removed_xpath_nodes' in feed:
            nodes = feed.pop('removed_xpath_nodes')
        else:
            nodes = None
        blog_feed = spider_pb2.BlogFeed(**feed)
        if nodes:
            blog_feed.removed_xpath_nodes.extend(nodes)
        stub = create_grpc_stub()
        try:
            result = stub.SubmitBlogFeed(blog_feed)
        except Exception as e:
            return {'message': f'unknow error[{e}]'}, 400
        if result.error:
            return {'message': result.message}, 400
        else:
            return '', 200
