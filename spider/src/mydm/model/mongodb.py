# -*- coding: utf-8 -*-


import logging
from datetime import datetime

from pymongo import MongoClient, ASCENDING
from scrapy.utils.project import get_project_settings


logger = logging.getLogger(__name__)


class MongoDB:

    def __init__(self):
        self._db = None

    def _create_indexes(self):
        db = self._db
        feed = db['feed']
        feed.create_index('url', name='idx_url')
        article = db['article']
        article.create_index('crawl_date', name='idx_crawl_date')
        article.create_index(
                [('spider', ASCENDING), ('crawl_date', ASCENDING)],
                name='idx_spider_crawl_date'
        )

    def _connect(self):
        settings = get_project_settings()
        while True:
            try:
                client = MongoClient(settings['MONGODB_URI'],
                                     serverSelectionTimeoutMS=2000)
                client.server_info()
            except:
                logger.info('waiting mongo online...')
                continue
            name = settings['MONGODB_URI'].split('/')[-1]
            db = client[name]
            self._db = db
            self._create_indexes()
            return

    def __getattr__(self, key):
        if self._db is None:
            self._connect()
        try:
            return self._db[key]
        except KeyError:
            raise AttributeError(f'collection[{key}] not found')


ScrapyDB = MongoDB()


def is_exists_article(item):
    result = ScrapyDB.article.count_documents(
        {
            'spider': item['spider'],
            'title': item['title'],
        }
    )
    if result > 0:
        return True
    return False


def save_article(item):
    if is_exists_article(item):
        return
    ScrapyDB.article.insert_one(item)


def get_spider_by_url(url):
    spider = ScrapyDB.spider.find_one(
            {
                'start_urls': {'$in': [url]}
            }
    )
    if spider is None:
        return
    return spider['_id']


def save_spider_settings(settings):
    try:
        del settings['_id']
    except KeyError:
        pass
    url = settings['start_urls'][0]
    spid = get_spider_by_url(url)
    if spid is None:
        ScrapyDB.spider.insert_one(settings)
    else:
        ScrapyDB.spider.update_one(
                {
                    '_id': spid
                },
                {
                    "$set": settings
                }
        )


def get_spider_settings():
    settings = []
    cursor = ScrapyDB.spider.find()
    for item in cursor:
        setting = dict(item)
        settings.append(setting)
    return settings
