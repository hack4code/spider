# -*- coding: utf-8 -*-


import logging
from flask import Flask, render_template
from error import NotFound, BadRequest

# DEBUG = True

# config for mongodb
MONGODB_URI = 'mongodb://mongodb:27017/'
MONGODB_STOREDB_NAME = 'articles'
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

# config for logging
if not app.debug:
    h = logging.FileHandler(app.config['LOG_FILE'],
                            encoding='utf-8')
    h.setLevel(logging.WARNING)
    h.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(h)
else:
    print("Flask in debugging mode...")


# error handler
@app.errorhandler(NotFound)
@app.errorhandler(BadRequest)
def error(error):
    code = error.status_code
    return render_template("error.html",
                           status_code=code,
                           message=error.message), code


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

from j import day_page
app.register_blueprint(day_page, url_prefix='/j')
