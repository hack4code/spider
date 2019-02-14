# -*- coding: utf-8 -*-


from collections import namedtuple
from datetime import datetime, date

from bson.errors import InvalidId
from bson.objectid import ObjectId

from flask import current_app, request, session

from flask_restful import Resource

from model import (
        get_article, vote_article,
        get_begin_day, get_before_day, get_after_day,
        get_last_aid, get_first_aid,
        get_entries, get_entries_next, get_entries_pre, get_entries_spider,
        get_spiders,
)


Spider = namedtuple('Spider', ['id', 'source'])


class Vote(Resource):

    def post(self):
        if 'uid' not in session:
            return {'message': 'no uid'}, 401

        try:
            aid = request.form['aid']
        except KeyError:
            return {'message': 'no aid'}, 400

        try:
            aid = ObjectId(aid)
        except InvalidId:
            return {'message': 'invalid aid'}, 400

        a = get_article(aid)

        if a:
            vote_article(a)
            return {'aid': str(aid)}, 200
        else:
            return {'message': 'article not existed'}, 400


class Day(Resource):

    def get(self):
        try:
            day = request.args['day']
        except KeyError:
            return {'message': 'argument day not found'}, 400
        else:
            try:
                day_entry = date(*(int(item) for item in day.split('-')))
            except ValueError:
                return {'message': 'invalid date value'}, 400

        day_begin = get_begin_day()

        if day_begin is None:
            return {'message': 'no articles found'}, 204

        if not day_begin <= day_entry <= datetime.utcnow().date():
            return {'message': 'no articles found'}, 204

        entries = get_entries(day_entry) or None

        day_before = get_before_day(day_entry)
        if day_before is not None:
            day_before = day_before.strftime('%Y-%m-%d')
        day_after = get_after_day(day_entry)
        if day_after is not None:
            day_after = day_after.strftime('%Y-%m-%d')

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
        try:
            spid = request.args['spid']
        except KeyError:
            return {'message': 'spider id not found'}, 400

        spiders = get_spiders()
        if spid not in spiders:
            return {'message': 'invalid spider id'}, 400

        lastaid = get_last_aid(spid)
        firstaid = get_first_aid(spid)
        try:
            aid = request.form['aid']
        except KeyError:
            entries = get_entries_spider(spid)
        else:
            try:
                aid = ObjectId(aid)
            except InvalidId:
                return {'message': 'invalid aid'}, 400

            if not firstaid <= aid <= lastaid:
                return {'message': 'aid not found'}, 400

            q = request.form.get('q', None)
            if q == 'p':
                entries = get_entries_pre(spid, aid)
            else:
                entries = get_entries_next(spid, aid)

        if entries:
            return {'spider': Spider(spid, spiders[spid]), 'entries': entries}
        else:
            return {'message': 'articles not found'}, 400
