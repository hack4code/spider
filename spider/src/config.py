# -*- coding: utf-8 -*-


# scrapy settings
BOT_NAME = 'AtomSpiders'
SPIDER_LOADER_CLASS = 'mydm.spiderloader.MongoSpiderLoader'

# header
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0'

# log
LOG_ENABLED = True
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s-%(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
LOG_STDOUT = True

ITEM_PIPELINES = {
    'mydm.pipelines.ContentPipeline': 255,
    'mydm.pipelines.ImagesDlownloadPipeline': 300,
    'mydm.pipelines.StorePipeline': 999
}

#
WEBSERVICE_ENABLED = False
TELNETCONSOLE_ENABLED = False

"""
spider settings
"""
LOGGER_NAME = 'AtomSpider'

# grpc
GRPC_URI = '[::]:50051'

# mongodb
MONGODB_URI = 'mongodb://scrapy:scrapy@mongodb:27017/scrapy'

# image pipeline
IMAGE_OPTIMIZE_CATEGORY_FILTER = ['漫画']
