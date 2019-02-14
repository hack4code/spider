# -*- coding: utf-8 -*-


import os
import logging
from datetime import datetime
from collections import namedtuple

from werkzeug.exceptions import NotFound, BadRequest
from flask import Flask, render_template

from converter import init_converter
from model import init_db, get_article, get_spiders
from api import init_api
from user import need_uid


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.logger.setLevel(logging.INFO)
# jinja
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
# converter
init_converter(app)
# db
init_db(app)
# api
init_api(app)


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


@app.route('/', methods=['GET'])
def home():
    today = datetime.utcnow().date()
    return entries_by_day(today)


@app.route('/d/<date:day>', methods=['GET'])
@need_uid
def entries_by_day(day):
    return render_template('day.html', day_entry=day)


@app.route('/a/<id:aid>', methods=['GET'])
def article(aid):
    a = get_article(aid)
    if a is None:
        raise NotFound(f'article[{aid}] not existed')

    def get_css(dom):
        path = '{}/css/{}.css'.format(app.static_folder, dom)
        return '{}.css'.format(dom) if os.path.isfile(path) else None

    return render_template(
            'article.html',
            article=a,
            dom_css=get_css(a.domain)
    )


Spider = namedtuple('Spider', ['id', 'source'])


@app.route('/p/<id:spid>', methods=['GET'])
def entries_by_spider(spid):
    spid = str(spid)
    spiders = get_spiders()
    if spid not in spiders:
        raise NotFound(f'spider[{spid}] not existed')
    return render_template('entries.html', spider=Spider(spid, spiders[spid]))


@app.route('/l/p', methods=['GET'])
def spiders():
    return render_template('spiders.html')


@app.route('/feed/rss', methods=['GET'])
def sumbit_atom_feed():
    return render_template('rss.html')


@app.route('/feed/blog', methods=['GET'])
def submit_blog_feed():
    return render_template('blog.html')
