# -*- coding: utf-8 -*-


from datetime import datetime, date
from collections import namedtuple

from bson.objectid import ObjectId
from bson.errors import InvalidId

from flask import current_app, request, session
from flask_restful import Resource


Spider = namedtuple('Spider', ['id', 'source'])


def _is_master():
    try:
        master = request.headers['master']
    except KeyError:
        master = 'no'
    return True if master.lower() == 'yes' else False


class Vote(Resource):

    def post(self):
        from model import get_article, vote_article

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
            return {'message': 'no article'}, 400


class Day(Resource):

    def get(self):
        from model import (
                get_begin_day, get_entries, get_before_day, get_after_day
        )

        try:
            day = request.args['day']
        except KeyError:
            return {'message': 'no day'}, 400
        else:
            try:
                day_entry = date(*(int(_) for _ in day.split('-')))
            except ValueError:
                return {'message': 'invalid day'}, 400

        day_begin = get_begin_day()

        if day_begin is None:
            return {'message': 'no articles'}, 204

        if not day_begin <= day_entry <= datetime.utcnow().date():
            return {'message': 'no articles'}, 204

        entries = get_entries(day_entry)

        if not _is_master() and entries:
            entries_ = {}
            for category, alist in entries.items():
                entries_[category] = [
                    a
                    for a in alist
                    if a.spider not in current_app.config['FEED_FILTER']
                ]
            entries = entries_

        day_before = get_before_day(day_entry)
        if day_before is not None:
            day_before = day_before.strftime('%Y-%m-%d')
        day_after = get_after_day(day_entry)
        if day_after is not None:
            day_after = day_after.strftime('%Y-%m-%d')

        return {'day_before': day_before,
                'day_after': day_after,
                'data': entries}


class Categories(Resource):

    def get(self):
        return {'data': list(current_app.config['ARTICLE_CATEGORIES'])}


class Entries(Resource):

    def get(self):
        from model import (
            get_spiders, get_last_aid, get_first_aid,
            get_entries_next, get_entries_pre, get_entries_spider
        )

        try:
            spid = request.args['spid']
        except KeyError:
            return {'message': 'no spider id'}, 400

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
            return {'message': 'no article found'}, 400


class Spider(Resource):

    def get(self):
        from model import get_spiders

        spiders = get_spiders()

        if _is_master():
            entries = [Spider(spid, name) for spid, name in spiders.items()]
        else:
            entries = [
                Spider(spid, name)
                for spid, name in spiders.items()
                if spid not in current_app.config['FEED_FILTER']
            ]
        return {'entries': entries}
