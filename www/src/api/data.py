# -*- coding: utf-8 -*-


from datetime import datetime
from collections import namedtuple

from bson.errors import InvalidId
from bson.objectid import ObjectId

from marshmallow import (
        Schema, fields, validates, ValidationError
)
from flask_restful import Resource
from flask import current_app, request, session

from model import (
        get_article,
        get_begin_day, get_before_day, get_after_day,
        get_entries_by_day,
        get_entries_next, get_entries_pre, get_entries_by_spider,
        get_spiders,
        get_categories
)
from .utils import format_messages


Spider = namedtuple('Spider', ['id', 'source'])


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
            def validate_day(self, day):
                day_begin = get_begin_day()
                if not day_begin <= day <= datetime.utcnow().date():
                    raise ValidationError('invalid day value')

        schema = DayRequestSchema()
        try:
            day_request = schema.load(request.args)
        except ValidationError as err:
            return {'message': format_messages(err.messages)}, 400
        except Exception as e:
            current_app.logger.exception('request args exception:')
            return {'message': 'invalid request'}, 400

        day_entry = day_request['day']
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


class Spiders(Resource):

    def get(self):
        spiders = get_spiders()
        entries = [
            Spider(spid, name)
            for spid, name in spiders.items()
        ]
        return {'entries': entries}


class Entries(Resource):

    def get(self):

        class EntryRequestScheme(Schema):
            spid = ObjectIdField(required=True)
            aid = ObjectIdField()
            q = fields.String()

            @validates('q')
            def validate_q(self, q):
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
        spiders = get_spiders()
        return {'spider': Spider(spid, spiders[spid]), 'entries': entries}


class Categories(Resource):
    categories = set([
        '新闻',
        '数据库',
        '安全',
        'Python',
        '技术',
        '科普',
    ])
    def get(self):
        result = get_categories()
        categories = categories | set(result)
        return {'data': categories}


