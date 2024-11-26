# -*- coding: utf-8 -*-


import os
import logging
from datetime import datetime

from werkzeug.exceptions import NotFound, BadRequest
from flask import Flask, render_template

from converter import init_converter
from model import init_db, get_article, get_spider
from api import init_api


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
def entries_by_day(day):
    return render_template('day.html', day_entry=day)


@app.route('/a/<id:aid>', methods=['GET'])
def article(aid):
    a = get_article(aid)
    if a is None:
        raise NotFound(f'article[{aid}] not existed')

    def get_site_css(site):
        path = f'{app.static_folder}/css/site/{site}.css'
        if not os.path.isfile(path):
            return
        return f'{site}.css'

    def get_site_script(site):
        path = f'{app.static_folder}/script/site/{site}.script'
        if not os.path.isfile(path):
            return
        with open(path) as f:
            return f.read().strip()

    site = a.domain
    headlist = a.head
    sitecss = get_site_css(site)
    return render_template(
            'article.html',
            article=a,
            sitecss=sitecss,
            sitescript=None,
            headlist=headlist,
    )


@app.route('/p/<id:spid>', methods=['GET'])
def entries_by_spider(spid):
    spider = get_spider(spid)
    if spider is None:
        raise NotFound(f'spider[{spid}] not existed')
    return render_template('entries.html', spider=spider)


@app.route('/l/p', methods=['GET'])
def spiders():
    return render_template('spiders.html')


@app.route('/feed/xml', methods=['GET'])
def atom_feed():
    return render_template('rss.html')

@app.route('/feed/xml/<id:spid>', methods=['GET'])
def atom_feed_edit(spid):
    return render_template('rss.html')
