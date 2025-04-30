# -*- coding: utf-8 -*-


import logging
from zoneinfo import ZoneInfo
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
    today = datetime.now(ZoneInfo("Asia/Shanghai")).date()
    return render_template('day.html', day_entry=today)


@app.route('/d/<date:day>', methods=['GET'])
def entries_by_day(day):
    return render_template('day.html', day_entry=day)


@app.route('/a/<id:aid>', methods=['GET'])
def article(aid):
    if (a := get_article(aid)) is None:
        raise NotFound(f'article[{aid}] not existed')
    spid = a['spider']
    spider = get_spider(spid)
    css = spider.get('css', None)
    return render_template(
        'article.html',
        article=a,
        css=css
    )


@app.route('/p/<id:spid>', methods=['GET'])
def entries_by_spider(spid):
    if (spider := get_spider(spid)) is None:
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
