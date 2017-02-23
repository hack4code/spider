# -*- coding: utf-8 -*-

"""
    flask config
"""
# cookie
SECRET_KEY = 'qweasdzxcrty'

# log
LOGGER_HANDLER_POLICY = 'always'

"""
    app config
"""
# mongodb
MONGODB_URI = 'mongodb://mongodb:27017/'
MONGODB_STOREDB_NAME = 'scrapy'
MONGODB_SCOREDB_NAME = 'score'
MONGODB_USER = 'flask'
MONGODB_PWD = 'flask'

# rabbitmq
BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbitmq:5672/'
CRAWL_KEY = 'crawl'
LXMLSPIDER_KEY = 'lxmlspider'
BLOGSPIDER_KEY = 'blogspider'

# category
ARTICLE_CATEGORIES = {u'技术',
                      u'数据库',
                      u'安全',
                      u'科技',
                      u'新闻'}

# filter
FEED_FILTER = []
