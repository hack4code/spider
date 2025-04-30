# -*- coding: utf-8 -*-


from datetime import datetime

from bson.errors import InvalidId
from bson.objectid import ObjectId

from marshmallow import (
    Schema, fields, validates, ValidationError
)
from flask_restful import Resource
from flask import current_app, request

from model import (
    get_begin_day, get_before_day, get_after_day,
    get_entries_by_day,
    get_entries_next, get_entries_pre, get_entries_by_spider,
    get_spider, get_spiders,
    get_categories
)
from .utils import format_messages


class ObjectIdField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return ObjectId(value)
        except InvalidId:
            raise ValidationError(f'invalid ObjectId {value}')


class Day(Resource):
    def get(self):
        class DayRequestSchema(Schema):
            day = fields.Date(required=True)

            @validates('day')
            def validate_day(self, day, data_key):
                day_begin = get_begin_day()
                if not day_begin <= day <= datetime.utcnow().date():
                    raise ValidationError('invalid day value')

        schema = DayRequestSchema()
        try:
            args = schema.load(request.args)
        except ValidationError as err:
            return {'message': format_messages(err.messages)}, 400
        except Exception:
            current_app.logger.exception('request args exception:')
            return {'message': 'invalid request'}, 400

        day_entry = args['day']
        day_before = get_before_day(day_entry)
        if day_before is not None:
            day_before = day_before.strftime('%Y-%m-%d')
        day_after = get_after_day(day_entry)
        if day_after is not None:
            day_after = day_after.strftime('%Y-%m-%d')
        entries = get_entries_by_day(day_entry)
        return {
            'day_before': day_before,
            'day_after': day_after,
            'data': entries,
        }


class Spider(Resource):
    def get(self):
        class SpiderRequestSchema(Schema):
            spid = ObjectIdField(required=True)

        schema = SpiderRequestSchema()
        try:
            args = schema.load(request.args)
        except ValidationError as err:
            return {'message': format_messages(err.messages)}, 400
        except Exception:
            current_app.logger.exception('request args exception:')
            return {'message': 'invalid request'}, 400
        spid = args['spid']
        spider = get_spider(spid)
        if spider is None:
            return {'message': f'spider[{spid}] not existed'}, 400
        return spider


class Spiders(Resource):
    def get(self):
        spiders = get_spiders()
        return spiders


class Entries(Resource):
    def get(self):
        class EntryRequestScheme(Schema):
            spid = ObjectIdField(required=True)
            aid = ObjectIdField()
            q = fields.String()

            @validates('q')
            def validate_q(self, q, data_key):
                if q not in ('p', 'n'):
                    raise ValidationError('invalid q value')

        schema = EntryRequestScheme()
        try:
            entry_request = schema.load(request.args)
        except ValidationError as err:
            return {'message': format_messages(err.messages)}, 400
        except Exception:
            return {'message': 'invalid request argument'}, 400

        spid = entry_request.get('spid')
        aid = entry_request.get('aid', None)
        q = entry_request.get('q', 'n')
        if aid is None:
            entries = get_entries_by_spider(spid)
        elif q == 'p':
            entries = get_entries_pre(spid, aid)
        elif q == 'n':
            entries = get_entries_next(spid, aid)

        if not entries:
            return {'message': 'no articles found'}, 400

        spid = str(spid)
        spider = get_spider(spid)
        return {'spider': spider, 'entries': entries}


class Categories(Resource):
    def get(self):
        categories = set([
            '新闻',
            '数据库',
            '安全',
            'Python',
            '技术',
            '科普',
        ])
        result = get_categories()
        categories = categories | set(result)
        return {'data': list(categories)}
