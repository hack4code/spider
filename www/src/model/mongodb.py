# -*- coding: utf-8 -*-


from collections import defaultdict
from datetime import datetime, timedelta

from pymongo import MongoClient, ASCENDING, DESCENDING

from .mongodata import Entry, EntryDay, Article, Spider, AID


class MongoDB:

    def __init__(self, name, config):
        self._name = name
        self._db = None
        self._config = config

    def _connect(self):
        config = self._config
        client = MongoClient(config['MONGODB_URI'], connect=False)
        db = client[self._name]
        db.authenticate(config['MONGODB_USER'], config['MONGODB_PWD'])
        self._db = db

    def __getattr__(self, key):
        if self._db is None:
            self._connect()
        try:
            return self._db[key]
        except KeyError:
            raise AttributeError(
                ('{} db has no collection {}').format(self._name, key)
            )


def init_db(app):
    global ScrapyDB, ScoreDB

    config = app.config
    ScrapyDB = MongoDB(config['MONGODB_STOREDB_NAME'], config)
    ScoreDB = MongoDB(config['MONGODB_SCOREDB_NAME'], config)


def get_begin_day():
    cursor = ScrapyDB.article.find(
        {},
        {'crawl_date': 1}
    ).sort(
        'crawl_date',
        ASCENDING,
    ).limit(1)
    if 0 == cursor.count():
        return
    return cursor[0]['crawl_date'].date()


def get_end_day():
    cursor = ScrapyDB.article.find(
        {},
        {'crawl_date': 1}
    ).sort(
        'crawl_date',
        DESCENDING
    ).limit(1)
    if 0 == cursor.count():
        return
    return cursor[0]['crawl_date'].date()


def get_spider_score(spids):
    cursor = ScoreDB.spider.find(
        {
            'id': {'$in': spids}
        },
        {
            'id': 1,
            'score': 1
        }
    )
    return {item['id']: item['score'] for item in cursor}


def get_article_score(aids):
    cursor = ScoreDB.article.find(
        {
            'id': {'$in': aids}
        },
        {
            'id': 1,
            'score': 1
        }
    )
    return {item['id']: item['score'] for item in cursor}


def get_score(entries):
    spscores = get_spider_score(list({_.spider for _ in entries}))
    ascores = get_article_score(list({_.id for _ in entries}))
    max_spscore = max(
            spscores.items(),
            key=lambda i: i[1]
    )[1] if spscores else 1.0
    max_ascore = max(
            ascores.items(),
            key=lambda i: i[1]
    )[1] if ascores else 1.0

    def get_score(e):
        return (10.0*spscores.get(e.spider, 0)/max_spscore +
                90.0*ascores.get(e.id, 0)/max_ascore)

    return {item.id: get_score(item) for item in entries}


def get_entries(day):
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
    entries_ = [EntryDay(item) for item in cursor]
    scores = get_score(entries_)
    entries = defaultdict(list)
    for e in sorted(entries_, key=lambda i: scores[i.id], reverse=True):
        entries[e.category].append(e)
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
    if 0 == cursor.count():
        return
    return cursor[0]['crawl_date'].date()


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
    if 0 == cursor.count():
        return
    return cursor[0]['crawl_date'].date()


"""
" spider category
"""


def get_spiders():
    cursor = ScrapyDB.spider.find({}, {'title': 1})
    return {str(item['_id']): item['title'] for item in cursor}


def get_spider(spid):
    cursor = ScrapyDB.spider.find(
            {
                '_id': spid
            },
            {
                'title': 1,
            }
    )
    if 0 == cursor.count():
        return
    spider = cursor[0]
    return Spider(spider['_id'], spider['title'])


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
    if 0 == cursor.count():
        return
    return cursor[0]['_id']


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
    if 0 == cursor.count():
        return
    return cursor[0]['_id']


def get_crawl_date(aid):
    cursor = ScrapyDB.article.find(
        {
            '_id': aid
        },
        {
            'crawl_date': 1
        }
    )
    if 0 == cursor.count():
        return
    return cursor[0]['crawl_date']


def get_entries_next(spid, aid):
    cursor = ScrapyDB.article.find(
        {
            '_id': {'$lt': aid},
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
    if 0 == cursor.count():
        return
    return [Entry(item) for item in cursor]


def get_entries_pre(spid, aid):
    cursor = ScrapyDB.article.find(
        {
            '_id': {'$gt': aid},
            'spider': spid
        },
        {
            '_id': 1,
            'title': 1
        }
    ).sort('_id', ASCENDING).limit(100)
    if 0 == cursor.count():
        return
    return list(reversed([Entry(item) for item in cursor]))


def get_entries_spider(spid):
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
    if 0 == cursor.count():
        return
    return [Entry(item) for item in cursor]


def get_article(aid):
    cursor = ScrapyDB.article.find(
        {
            '_id': aid
        },
        {
            'title': 1,
            'domain': 1,
            'link': 1,
            'content': 1,
            'lang': 1,
            'source': 1,
            'spider': 1
        }
    ).limit(1)
    if 0 == cursor.count():
        return
    return Article(cursor[0])


def vote_article(a):
    ScoreDB.article.update(
        {
            'id': a.id
        },
        {
            '$inc': {'score': 1}
        },
        upsert=True
    )
    ScoreDB.spider.update(
        {
            'id': a.spider
        },
        {
            '$inc': {'score': 1}
        },
        upsert=True
    )


def get_categories():
    return ScrapyDB.article.distinct('category')


# function for test

def get_aids_by_category(c):
    cursor = ScrapyDB.article.find(
        {
            'category': c
        },
        {
            '_id': 1
        }
    ).sort('_id', ASCENDING)
    if 0 == cursor.count():
        return
    return [AID(item['_id']) for item in cursor]


def get_all_aids():
    cursor = ScrapyDB.article.find(
        {},
        {
            '_id': 1
        }
    )
    if 0 == cursor.count():
        return
    return [item['_id'] for item in cursor]
