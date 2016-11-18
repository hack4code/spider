# -*- coding: utf-8 -*-

BOT_NAME = 'mydm'
SPIDER_LOADER_CLASS = 'mydm.spiderloader.MongoSpiderLoader'

DOWNLOAD_DELAY = 0.6
CONCURRENT_REQUESTS_PER_DOMAIN = 5
WEBSERVICE_ENABLED = False
TELNETCONSOLE_ENABLED = False

LOG_ENABLED = True
LOG_LEVEL = 'INFO'
LOG_STDOUT = False

ITEM_PIPELINES = {
    'mydm.pipelines.ContentPipeline': 255,
    'mydm.pipelines.ImagesDlownloadPipeline': 300,
    'mydm.pipelines.StorePipeline': 999
}

DOWNLOADER_MIDDLEWARES = {
    'mydm.middlewares.ETagMiddleware': 300
}

"""

"""
# config for mongodb
MONGODB_URI = 'mongodb://mongodb:27017/'
MONGODB_DB_NAME = 'articles'
MONGODB_ARTICLE_COLLECTION_NAME = 'article'
MONGODB_FEED_COLLECTION_NAME = 'feed'
MONGODB_SPIDER_COLLECTION_NAME = 'spider'
MONGODB_USER = 'scrapy'
MONGODB_PWD = 'scrapy'

# config for celery
BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbitmq:5672//'

# config for failed task
RETRY_SPIDERS_URL = 'redis://redis:6379/0'
# config for etag
ETAG_URL = 'redis://redis:6379/1'
# config for spider task
TEMP_SPIDER_STATS_URL = 'redis://redis:6379/2'

# config for if-modify-since
MODIFY_DELTA = 1

# category
ARTICLE_CATEGORIES = [u'技术',
                      u'数据库',
                      u'安全',
                      u'科技',
                      u'新闻']
