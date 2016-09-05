# -*- coding: utf-8 -*-


from datetime import datetime
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings


settings = get_project_settings()


class MongoDB(object):
    COLLECTIONS = ('article', 'feed', 'spider', 'category')

    def __init__(self):
        self.db = None
        self.client = MongoClient(settings['MONGODB_URI'], connect=False)

    def connect(self):
        db = self.client[settings['MONGODB_DB_NAME']]
        db.authenticate(settings['MONGODB_USER'], settings['MONGODB_PWD'])
        feed = db['feed']
        feed.ensure_index('url', name='idx_url')
        article = db['article']
        article.ensure_index('crawl_date', name='idx_crawl_date')
        article.ensure_index('spider', name='idx_spider')
        self.db = db

    def __getattr__(self, key):
        if self.db is None:
            self.connect()
        if key in self.COLLECTIONS:
            return self.db[key]
        else:
            raise AttributeError(
                'articles db has no collection {}'.format(key))


db = MongoDB()


def is_exists_feed(url):
    cursor = db.feed.find({'url': url}).limit(1)
    return False if cursor.count() == 0 else True


def save_feed(url):
    result = db.feed.insert_one(
        {
            'url': url,
            'create_date': datetime.now()
        }
    )
    return result.inserted_id


def _get_item_day_begin(item):
    d = item['crawl_date']
    t = datetime(d.year,
                 d.month,
                 d.day,
                 0,
                 0,
                 0,
                 0)
    return t


def is_exists_article(item):
    t = _get_item_day_begin(item)
    cursor = db.article.find(
        {
            'title': item['title'],
            'domain': item['domain'],
            'source': item['source'],
            'crawl_date': {'$lt': t}
        }
    ).limit(1)
    if cursor.count() > 0:
        return True
    cursor = db.article.find(
        {
            'title': item['title'],
            'crawl_date': {'$gte': t}
        },
        {
            'content': 1
        }
    ).limit(1)
    if (cursor.count() > 0 and
       len(cursor[0]['content']) > len(item['content'])):
            return True
    return False


def save_article(item):
    t = _get_item_day_begin(item)
    result = db.article.update(
        {
            'title': item['title'],
            'crawl_date': {'$gte': t}
        },
        item,
        upsert=True
    )
    return result


def is_exists_spider(url):
    cursor = db.spider.find({'start_urls': {'$in': [url, ]}})
    return True if cursor.count() > 0 else False


def save_spider_settings(settings):
    result = db.spider.insert_one(settings)
    return result.inserted_id


def get_spider_settings():
    sp_settings = []
    cursor = db.spider.find()
    for r in cursor:
        setting = dict(r)
        setting['_id'] = str(r['_id'])
        sp_settings.append(setting)
    return sp_settings


def get_category_tags():
    cursor = db.category.find()
    return {r['category']: r['tags'] for r in cursor}
