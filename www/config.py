# -*- coding: utf-8 -*-


# cookie
SECRET_KEY = 'qweasdzxcrty'

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

# log
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s-%(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

ARTICLE_CATEGORIES = {u'技术',
                      u'数据库',
                      u'安全',
                      u'科技',
                      u'新闻'}
