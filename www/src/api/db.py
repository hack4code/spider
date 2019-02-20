# -*- coding: utf-8 -*-


from datetime import datetime
from collections import namedtuple

from bson.errors import InvalidId
from bson.objectid import ObjectId

from marshmallow import (
        Schema, fields, validates, post_load, ValidationError
)
from flask_restful import Resource

from flask import current_app, request, session


from model import (
        get_article, vote_article,
        get_begin_day, get_before_day, get_after_day,
        get_last_aid, get_first_aid,
        get_entries, get_entries_next, get_entries_pre, get_entries_spider,
        get_spiders,
)


Spider = namedtuple('Spider', ['id', 'source'])


class ObjectIdField(fields.Field):

    def _serialize(self, value, attr, obj, **kwargs):
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return ObjectId(value)
        except InvalidId:
            raise ValidationError(f'invalid ObjectId {value}')


class Vote(Resource):

    def post(self):

        class VoteRequestSchema(Schema):
            aid = ObjectIdField(required=True)

        def __init__(self, strict=True, **kwargs):
            super().__init__(strict=strict, **kwargs)

        if 'uid' not in session:
            return {'message': 'no uid'}, 401

        schema = VoteRequestSchema()
        try:
            vote_request = schema.load(request.get_json()).data
        except ValidationError as err:
            return {'message': err.message['_schema']}, 400
        except Exception:
            return {'message': 'invalid request'}, 400

        aid = vote_request['aid']
        a = get_article(aid)

        if not a:
            return {'message': 'article not existed'}, 400

        vote_article(a)
        return {'aid': str(aid)}, 200


class Day(Resource):

    def get(self):

        class DayRequestSchema(Schema):
            day = fields.Date(required=True)

            def __init__(self, strict=True, **kwargs):
                super().__init__(strict=strict, **kwargs)

            @validates('day')
            def validate_day(self, day):
                day_begin = get_begin_day()
                if not day_begin <= day <= datetime.utcnow().date():
                    raise ValidationError('invalid day value')

        schema = DayRequestSchema()
        try:
            day_request = schema.load(request.args).data
        except ValidationError as err:
            return {'message': err.message['_schema']}, 400
        except Exception:
            return {'message': 'invalid request'}, 400

        day_entry = day_request['day']
        day_before = get_before_day(day_entry)
        if day_before is not None:
            day_before = day_before.strftime('%Y-%m-%d')
        day_after = get_after_day(day_entry)
        if day_after is not None:
            day_after = day_after.strftime('%Y-%m-%d')
        entries = get_entries(day_entry) or None
        return {
                'day_before': day_before,
                'day_after': day_after,
                'data': entries,
        }


class Categories(Resource):

    def get(self):
        return {'data': list(current_app.config['ARTICLE_CATEGORIES'])}


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
        spiders = get_spiders()

        class EntryRequestScheme(Schema):
            spid = fields.String(required=True)
            aid = fields.String()
            q = fields.String()

            def __init__(self, strict=True, **kwargs):
                super().__init__(strict=strict, **kwargs)

        @validates('spid')
        def validate_spid(self, spid):
            if spid not in spiders:
                raise ValidationError('invalid spider ID')
            try:
                ObjectId(spid)
            except InvalidId:
                raise ValidationError('invalid spider ID value')

        @validates('q')
        def validate_q(self, q):
            if q not in ('p', 'n'):
                raise ValidationError('invalid q value')

        @post_load
        def validate_aid(self, data):
            spid = data['spid']
            aid = data.get('aid', None)
            if aid is None:
                return
            try:
                aid = ObjectId(aid)
            except InvalidId:
                raise ValidationError(f'invalid aid value {aid}')
            last_aid = get_last_aid(spid)
            first_aid = get_first_aid(spid)
            if not first_aid <= aid <= last_aid:
                raise ValidationError(f'aid {aid} not existed')

        schema = EntryRequestScheme()
        try:
            entry_request = schema.load(request.args).data
        except ValidationError as err:
            return {'message': err.messages['_schema']}, 400
        except Exception:
            return {'message': 'invalid request argument'}, 400

        spid = entry_request.get('spid')
        aid = entry_request.get('aid', None)
        q = entry_request.get('q', None)
        if aid is None:
            entries = get_entries_spider(spid)
        elif q == 'p':
            entries = get_entries_pre(spid, aid)
        else:
            entries = get_entries_next(spid, aid)

        if not entries:
            return {'message': 'no articles found'}, 400

        return {'spider': Spider(spid, spiders[spid]), 'entries': entries}
