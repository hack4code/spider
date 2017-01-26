# -*- coding: utf-8 -*-


from datetime import datetime

from flask import Flask, render_template

from error import NotFound, BadRequest
from user import need_uid

# app init
app = Flask(__name__)
app.config.from_pyfile('config.py')

# config for jinja
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


# error handler
@app.errorhandler(NotFound)
@app.errorhandler(BadRequest)
def error(error):
    code = error.code
    return render_template("error.html",
                           status_code=code,
                           message=error.description), code

# converter
from util import DateConverter, IdConverter
app.url_map.converters['date'] = DateConverter
app.url_map.converters['id'] = IdConverter


@app.route('/', methods=['GET'])
def home():
    today = datetime.utcnow().date()
    return show_entries_byday(today)


@app.route('/d/<date:day>', methods=['GET'])
@need_uid
def show_entries_byday(day):
    return render_template('day.html',
                           day_entry=day)


@app.route('/a/<id:aid>', methods=['GET'])
def show_article(aid):
    from model import get_article

    a = get_article(aid)

    def get_css(dom):
        import os
        path = '{}/css/{}.css'.format(app.static_folder,
                                      dom)
        return '{}.css'.format(dom) if os.path.isfile(path) else None

    if a:
        return render_template('article.html',
                               article=a,
                               dom_css=get_css(a.domain))
    else:
        raise NotFound('article not exist')


@app.route('/p/<id:spid>', methods=['GET'])
def show_entries_byspider(spid):
    from collections import namedtuple
    from model import get_spiders

    Spider = namedtuple('Spider', ['id', 'source'])
    spid = str(spid)
    spiders = get_spiders()
    if spid in spiders:
        return render_template('entries.html',
                               spider=Spider(spid,
                                             spiders[spid]))
    else:
        raise BadRequest('spider id not existed')


@app.route('/l/p', methods=['GET'])
def spiders():
    return render_template('spiders.html')


@app.route('/feed/rss', methods=['GET'])
def atom():
    return render_template('rss.html')


@app.route('/feed/blog', methods=['GET'])
def blog():
    return render_template('blog.html')


from .api import api_page
app.register_blueprint(api_page, url_prefix='/api')

from .submit import submit_page
app.register_blueprint(submit_page, url_prefix='/submit')
