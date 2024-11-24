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


def is_exists_feed(url):
    result = ScrapyDB.feed.count_documents({'url': url})
    if result == 0:
        return False
    else:
        return True


def save_feed(url):
    result = ScrapyDB.feed.insert_one(
        {
            'url': url,
            'create_date': datetime.now()
        }
    )
    return result.inserted_id


def is_exists_article(item):
    day = datetime.combine(item['crawl_date'].date(), datetime.min.time())
    result = ScrapyDB.article.count_documents(
        {
            'spider': item['spider'],
            'crawl_date': {'$lt': day},
            'title': item['title'],
            'domain': item['domain'],
            'source': item['source']
        }
    )
    if result > 0:
        return True
    cursor = ScrapyDB.article.find(
        {
            'spider': item['spider'],
            'crawl_date': {'$gte': day},
            'title': item['title']
        },
        {
            'content': 1
        }
    ).limit(1)
    result = list(cursor)
    if (len(result) > 0 and
       len(result[0]['content']) > len(item['content'])):
        return True
    return False


def save_article(item):
    result = ScrapyDB.article.insert_one(item)
    return result


def is_exists_spider(url):
    result = ScrapyDB.spider.count_documents(
            {
                'start_urls': {'$in': [url]}
            }
    )
    if result == 0:
        return False
    else:
        return True


def save_spider_settings(settings):
    try:
        del settings['_id']
    except KeyError:
        pass
    result = ScrapyDB.spider.insert_one(settings)
    return result.inserted_id


def get_spider_settings():
    settings = []
    cursor = ScrapyDB.spider.find()
    for item in cursor:
        setting = dict(item)
        setting['_id'] = str(item['_id'])
        settings.append(setting)
    return settings
