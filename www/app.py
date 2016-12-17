# -*- coding: utf-8 -*-


from flask import Flask, render_template
from error import NotFound, BadRequest

# DEBUG = True

# config for mongodb
MONGODB_URI = 'mongodb://mongodb:27017/'
MONGODB_STOREDB_NAME = 'scrapy'
MONGODB_SCOREDB_NAME = 'score'
MONGODB_USER = 'flask'
MONGODB_PWD = 'flask'

# scrapy
FEED_SUBMIT_URL = 'http://gw:8001/feed'

# log
LOG_FILE = '/var/log/www/www.log'

# app init
app = Flask(__name__)
app.config.from_object(__name__)

# config for jinja
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# config for session
app.secret_key = 'qweasdzxcrty'


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

from home import home_page
app.register_blueprint(home_page, url_prefix='/home')
from a import article_page
app.register_blueprint(article_page, url_prefix='/a')
from p import spider_page
app.register_blueprint(spider_page, url_prefix='/p')
from d import entry_page
app.register_blueprint(entry_page, url_prefix='/d')
from l import list_page
app.register_blueprint(list_page, url_prefix='/l')
from f import feed_page
app.register_blueprint(feed_page, url_prefix='/f')
from api import api_page
app.register_blueprint(api_page, url_prefix='/api')
