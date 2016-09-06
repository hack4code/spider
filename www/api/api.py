# -*- coding: utf-8 -*-


import logging
import requests
from datetime import date
from flask import Blueprint, jsonify, request, session

from app import app
from model import format_aid, get_article, vote_article
from model import get_begin_day, get_entries, get_before_day, \
    get_after_day, get_categories


logger = logging.getLogger(__name__)


api_page = Blueprint('api_page',
                     __name__,
                     template_folder='template')


@api_page.route('/feed/rss', methods=['POST'])
def gen_atom_feed():
    try:
        url = '{}/atom'.format(app.config['FEED_SUBMIT_URL'])
        r = requests.post(url, request.form)
    except:
        logger.error('genspider[atom] error')
        return jsonify(err=1, msg='exception')
    rj = r.json()
    return jsonify(err=rj['err'], msg=rj['msg'])


@api_page.route('/feed/blog', methods=['POST'])
def gen_blog_feed():
    try:
        url = '{}/blog'.format(app.config['FEED_SUBMIT_URL'])
        r = requests.post(url, request.form)
    except:
        logger.error('genspider[blog] error')
        return jsonify(err=1, msg='exception')
    rj = r.json()
    return jsonify(err=rj['err'], msg=rj['msg'])


@api_page.route('/vote', methods=['POST'])
def vote():
    if 'uid' not in session:
        return jsonify(err=1, msg='no uid')
    if 'aid' not in request.form:
        return jsonify(err=2, msg='no aid')
    aid = request.form['aid']
    try:
        aid = format_aid(aid)
    except:
        return jsonify(err=3, msg='invalid aid')
    a = get_article(aid)
    if a is None:
        return jsonify(err=4, msg='no article')
    vote_article(a)
    return jsonify(err=0, aid=str(aid))


def get_day(day):
    y, m, d = [int(i) for i in day.split('-')]
    return date(y, m, d)


@api_page.route('/day', methods=['GET'])
def day_entries():
    try:
        day_entry = get_day(request.args.get('day', None))
    except:
        return jsonify(err=1, msg='invalid day')

    day_begin = get_begin_day()

    if day_begin is None or day_entry is None:
        return jsonify(err=1, msg='no articles')

    if day_entry < day_begin or day_entry > date.today():
        return jsonify(err=1, msg='no articles')

    entries = get_entries(day_entry)
    if len(entries) == 0:
        entries = None

    day_before = get_before_day(day_entry)
    if day_before is not None:
        day_before = day_before.strftime('%Y-%m-%d')
    day_after = get_after_day(day_entry)
    if day_after is not None:
        day_after = day_after.strftime('%Y-%m-%d')

    return jsonify(err=0,
                   day_before=day_before,
                   day_after=day_after,
                   data=entries)


@api_page.route('/categories', methods=['GET'])
def categories():
    categories = get_categories()
    return jsonify(err=0,
                   data=categories)


from collections import namedtuple
from model import get_spiders, get_last_aid, get_first_aid, \
    get_entries_next, get_entries_pre, get_entries_spider, \
    check_aid


Spider = namedtuple('Spider', ['id', 'source'])


@api_page.route('/spider', methods=['GET'])
def show_entries():
    spid = request.args.get('spid', None)
    if spid is None:
        return jsonify(err=1, msg='no spider id')
    spiders = get_spiders()
    if spid not in spiders:
        return jsonify(err=2, msg='invalid spider id')

    aid_last = get_last_aid(spid)
    aid_first = get_first_aid(spid)
    aid = request.args.get('aid', None)
    if aid:
        try:
            aid = format_aid(aid)
        except:
            return jsonify(err=3, msg='invalid aid')

        if not check_aid(aid, aid_first, aid_last):
            return jsonify(err=4, msg='aid not found')
        q = request.args.get('q', 'n')
        if q == 'n':
            entries = get_entries_next(spid, aid)
        elif q == 'p':
            entries = get_entries_pre(spid, aid)
    else:
        entries = get_entries_spider(spid)

    if entries is None or len(entries) == 0:
        return jsonify(err=5, msg='no article found')

    return jsonify(err=0,
                   spider=Spider(spid, spiders[spid]),
                   entries=entries)


@api_page.route('/spiders', methods=['GET'])
def spiders():
    spiders = get_spiders()
    entries = [Spider(spid, name) for spid, name in spiders.items()]
    return jsonify(err=0,
                   entries=entries)
