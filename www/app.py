# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from werkzeug.exceptions import NotFound, BadRequest
from flask import Flask, render_template
from flask_restful import Api

from user import need_uid
from util import DateConverter, IdConverter
from api import (
        Vote, Day, Categories, Entries, Spiders,
        CrawlSpiders, AtomFeed, BlogFeed
)


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.logger.setLevel(logging.INFO)

# jinja
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


# error handler
@app.errorhandler(NotFound)
@app.errorhandler(BadRequest)
def error(error):
    code = error.code
    return render_template(
            'error.html',
            status_code=code,
            message=error.description
    ), code


# converter
app.url_map.converters['date'] = DateConverter
app.url_map.converters['id'] = IdConverter


@app.route('/', methods=['GET'])
def home():
    today = datetime.utcnow().date()
    return show_entries_byday(today)


@app.route('/d/<date:day>', methods=['GET'])
@need_uid
def show_entries_byday(day):
    return render_template('day.html', day_entry=day)


@app.route('/a/<id:aid>', methods=['GET'])
def show_article(aid):
    from model import get_article
    import os

    a = get_article(aid)
    if a is None:
        raise NotFound('article not existed')

    def get_css(dom):
        path = '{}/css/{}.css'.format(app.static_folder, dom)
        return '{}.css'.format(dom) if os.path.isfile(path) else None

    return render_template(
            'article.html',
            article=a,
            dom_css=get_css(a.domain)
    )


@app.route('/p/<id:spid>', methods=['GET'])
def show_entries_byspider(spid):
    from collections import namedtuple
    from model import get_spiders

    Spider = namedtuple('Spider', ['id', 'source'])
    spid = str(spid)
    spiders = get_spiders()
    if spid not in spiders:
        raise NotFound('spider not existed')
    return render_template('entries.html', spider=Spider(spid, spiders[spid]))


@app.route('/l/p', methods=['GET'])
def show_spiders():
    return render_template('spiders.html')


@app.route('/feed/rss', methods=['GET'])
def sumbit_atom_feed():
    return render_template('rss.html')


@app.route('/feed/blog', methods=['GET'])
def submit_blog_feed():
    return render_template('blog.html')


# api
api = Api(app)
api.add_resource(Spiders, '/api/spiders')
api.add_resource(CrawlSpiders, '/submit/crawl')
api.add_resource(AtomFeed, '/submit/rss')
api.add_resource(BlogFeed, '/submit/blog')
api.add_resource(Vote, '/api/vote')
api.add_resource(Day, '/api/day')
api.add_resource(Entries, '/api/entries')
api.add_resource(Categories, '/api/categories')
