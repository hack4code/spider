# -*- coding: utf-8 -*-

# scrapy settings
BOT_NAME = 'BlogSpider'
SPIDER_LOADER_CLASS = 'mydm.spiderloader.MongoSpiderLoader'

CONCURRENT_ITEMS = 64
CONCURRENT_REQUESTS = 12
CONCURRENT_REQUESTS_PER_DOMAIN = 4
DNS_TIMEOUT = 180
DOWNLOAD_DELAY = 1

WEBSERVICE_ENABLED = False
TELNETCONSOLE_ENABLED = False

LOG_ENABLED = True
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s-%(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

EXTENSIONS = {
}

ITEM_PIPELINES = {
    'mydm.pipelines.ContentPipeline': 255,
    'mydm.pipelines.ImagesDlownloadPipeline': 300,
    'mydm.pipelines.StorePipeline': 999
}

DOWNLOADER_MIDDLEWARES = {
}

"""
spider settings
"""
LOGGER_NAME = 'mydm'

# grpc
GRPC_URI = '[::]:50051'

# mongodb
MONGODB_URI = 'mongodb://scrapy:scrapy@mongodb:27017/scrapy'

# image pipeline
IMAGE_OPTIMIZE_CATEGORY_FILTER = ['漫画']
