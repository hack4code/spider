# -*- coding: utf-8 -*-


import json

import pika

from flask import request, current_app

from marshmallow import (
        Schema, fields, validates, pre_load, post_load, ValidationError
)
from flask_restful import Resource


def _send(key, data):
    body = json.dumps(data)
    connection = pika.BlockingConnection(
        pika.connection.URLParameters('BROKER_URL')
    )
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_logs',
                             exchange_type='direct')
    channel.basic_publish(exchange='direct_logs',
                          routing_key=key,
                          body=body)
    connection.close()


class StripSchema(Schema):

    @pre_load
    def strip(self, data):
        new_data = {}
        for key, val in data.items():
            if isinstance(val, str):
                val = val.strip(' \r\t\n')
            elif isinstance(val, (list, tuple)):
                val = list(filter(lambda s: s,
                                  (item.strip(' \r\t\n') for item in val)))
            if val:
                new_data[key] = val
        return new_data


class SpiderListSchema(StripSchema):
    spiders = fields.List(fields.String())

    @post_load
    def spiders(self, data):
        try:
            return data['spiders']
        except KeyError:
            return []


class CrawlSpiders(Resource):

    def post(self):
        schema = SpiderListSchema()
        try:
            spiders = schema.loads(request.get_json()).data
        except Exception:
            return {'message': 'invalid spiders data'}, 400
        if not spiders:
            return {'message': 'no spider found'}, 400
        _send(current_app.config['CRAWL_KEY'], {'spiders': spiders})
        return '', 200


class FeedSchema(StripSchema):

    @validates('category')
    def validate_category(category):
        if category not in current_app.config['ARTICLE_CATEGORIES']:
            raise ValidationError(f'category value {category} is invalid')


class AtomFeedSchema(FeedSchema):
    url = fields.Url(required=True)
    category = fields.String(required=True)
    item_content_xpath = fields.String()
    removed_xpath_nodes = fields.List(fields.String())


class AtomFeed(Resource):

    def post(self):
        schema = AtomFeedSchema()
        try:
            feed = schema.loads(request.get_json()).data
        except ValidationError as err:
            return {'message': err.messages['_schema']}, 400
        except Exception:
            return {'message': 'invalid feed'}, 400
        current_app.logger.info(f'atom feed: {feed}')
        _send(current_app.config['LXMLSPIDER_KEY'], feed)
        return '', 200


class BlogFeedSchema(FeedSchema):
    url = fields.Url(required=True)
    category = fields.String(required=True)
    entry_xpath = fields.String(required=True)
    item_title_xpath = fields.String(required=True)
    item_link_xpath = fields.String(required=True)
    item_content_xpath = fields.String(required=True)
    removed_xpath_nodes = fields.List(fields.String())


class BlogFeed:

    def post(self):
        schema = BlogFeedSchema()
        try:
            feed = schema.loads(request.get_json()).data
        except ValidationError as e:
            return {'message': str(e)}, 400
        except Exception:
            return {'message': 'invalid blog feed'}, 400
        current_app.logger.info(f'blog feed: {feed}')
        _send(current_app.config['BLOGSPIDER_KEY'], feed)
        return '', 200
