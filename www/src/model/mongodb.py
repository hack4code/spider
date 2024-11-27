# -*- coding: utf-8 -*-


from datetime import datetime, timedelta

from flask import current_app
from pymongo import MongoClient, ASCENDING, DESCENDING

from .datatype import Entry, EntryDay, Article, Spider


class MongoDB:
    def __init__(self, uri):
        self._uri = uri
        self._dbname = uri.split('/')[-1]
        self.db = None

    def _connect(self):
        while True:
            try:
                client = MongoClient(self._uri,
                                     serverSelectionTimeoutMS=2000)
                client.server_info()
            except:
                current_app.logger.info('waiting mongodb online...')
                continue
            self.db = client[self._dbname]
            return

    def __getattr__(self, collection_name):
        if self.db is None:
            self._connect()
        try:
            return self.db[collection_name]
        except KeyError:
            raise AttributeError(
                    f'invalid collection {collection_name}'
            )


def init_db(app):
    global ScrapyDB
    ScrapyDB = MongoDB(app.config['SCRAPYDB_URI'])


def get_begin_day():
    cursor = ScrapyDB.article.find(
        {},
        {'crawl_date': 1}
    ).sort(
        'crawl_date',
        ASCENDING,
    ).limit(1)
    result = list(cursor)
    if 0 == len(result):
        return
    return result[0]['crawl_date'].date()


def get_end_day():
    cursor = ScrapyDB.article.find(
        {},
        {'crawl_date': 1}
    ).sort(
        'crawl_date',
        DESCENDING
    ).limit(1)
    result = list(cursor)
    if 0 == len(result):
        return
    return result[0]['crawl_date'].date()


def get_entries_by_day(day):
    begin = datetime(
            day.year,
            day.month,
            day.day,
            0,
            0,
            0,
            0
    )
    end = begin + timedelta(days=1)
    cursor = ScrapyDB.article.find(
        {
            'crawl_date': {'$gte': begin, '$lt': end}
        },
        {
            'title': 1,
            'category': 1,
            'source': 1,
            'tag': 1,
            'spider': 1,
            'domain': 1,
            'link': 1,
        }
    )
    entries = [EntryDay.from_item(item) for item in cursor]
    if not entries:
        return
    return entries


def get_before_day(day):
    t = datetime(
            day.year,
            day.month,
            day.day,
            0,
            0,
            0,
            0
    )
    cursor = ScrapyDB.article.find(
        {
            'crawl_date': {'$lt': t}
        },
        {
            'crawl_date': 1
        }
    ).sort('crawl_date', DESCENDING).limit(1)
    result = list(cursor)
    if 0 == len(result):
        return
    return result[0]['crawl_date'].date()


def get_after_day(day):
    t = datetime(
            day.year,
            day.month,
            day.day,
            0,
            0,
            0,
            0
    )
    nextday = t + timedelta(days=1)
    cursor = ScrapyDB.article.find(
        {
            'crawl_date': {'$gte': nextday}
        },
        {
            'crawl_date': 1
        }
    ).sort(
        'crawl_date',
        ASCENDING,
    ).limit(1)
    result = list(cursor)
    if 0 == len(result):
        return
    return result[0]['crawl_date'].date()


def get_spider(spid):
    spider = ScrapyDB.spider.find_one(
            {
                '_id': spid
            }
    )
    if spider is None:
        return
    return Spider.from_item(spider)


def get_spiders():
    cursor = ScrapyDB.spider.find({})
    return [Spider.from_item(item) for item in cursor]


def get_first_aid(spid):
    cursor = ScrapyDB.article.find(
        {
            'spider': spid
        },
        {
            '_id': 1
        }
    ).sort(
        '_id',
        ASCENDING
    ).limit(1)
    result = list(cursor)
    if 0 == len(result):
        return
    return result[0]['_id']


def get_last_aid(spid):
    cursor = ScrapyDB.article.find(
        {
            'spider': spid
        },
        {
            '_id': 1
        }
    ).sort(
        '_id',
        DESCENDING
    ).limit(1)
    result = list(cursor)
    if 0 == len(result):
        return
    return result[0]['_id']


def get_crawl_date(aid):
    cursor = ScrapyDB.article.find(
        {
            '_id': aid
        },
        {
            'crawl_date': 1
        }
    )
    result = list(cursor)
    if 0 == len(result):
        return
    return result[0]['crawl_date']


def get_entries_next(spid, aid):
    cursor = ScrapyDB.article.find(
        {
            '_id': {'$lt': aid},
            'spider': str(spid),
        },
        {
            '_id': 1,
            'title': 1
        }
    ).sort(
        '_id',
        DESCENDING
    ).limit(100)
    result = list(cursor)
    if 0 == len(result):
        return
    return [Entry.from_item(item) for item in result]


def get_entries_pre(spid, aid):
    cursor = ScrapyDB.article.find(
        {
            '_id': {'$gt': aid},
            'spider': str(spid),
        },
        {
            '_id': 1,
            'title': 1
        }
    ).sort('_id', ASCENDING).limit(100)
    result = list(cursor)
    if 0 == len(result):
        return
    return reversed(
        [Entry.from_item(item) for item in result]
    )


def get_entries_by_spider(spid):
    cursor = ScrapyDB.article.find(
        {
            'spider': spid
        },
        {
            '_id': 1,
            'title': 1
        }
    ).sort(
        '_id',
        DESCENDING
    ).limit(100)
    result = list(cursor)
    if 0 == len(result):
        return
    return [Entry.from_item(item) for item in result]


def get_article(aid):
    a = ScrapyDB.article.find_one(
        {
            '_id': aid
        }
    )
    if a is None:
        return
    return Article.from_item(a)


def get_categories():
    cursor = ScrapyDB.spider.distinct('category')
    return list(cursor)
