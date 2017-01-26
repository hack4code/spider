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
CRAWL_QUEUE_NAME = 'crawl_job_queue'
LXMLSPIDER_QUEUE_NAME = 'lxmlspider_job_queue'
BLOGSPIDER_QUEUE_NAME = 'blogspider_job_queue'

# log
LOG_FILE = '/var/log/www/www.log'
