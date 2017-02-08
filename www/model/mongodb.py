# -*- coding: utf-8 -*-


from collections import namedtuple, defaultdict
from datetime import datetime, timedelta
from html import unescape

from pymongo import MongoClient, ASCENDING, DESCENDING

from app import app


Entry = namedtuple('Entry', ['id',
                             'title'])

Entry_Day = namedtuple('Entry_Day', ['id',
                                     'title',
                                     'category',
                                     'source',
                                     'tag',
                                     'spider',
                                     'domain',
                                     'link'])


class MongoDB:
    def __init__(self, name):
        self._name = name
        self._client = MongoClient(app.config['MONGODB_URI'],
                                   connect=False)
        self._db = None

    def _connect(self):
        db = self._client[self._name]
        db.authenticate(app.config['MONGODB_USER'],
                        app.config['MONGODB_PWD'])
        self._db = db

    def __getattr__(self, key):
        if self._db is None:
            self._connect()
        try:
            return self._db[key]
        except KeyError:
            raise AttributeError((
                '{} db has no collection {}'
                ).format(self._name,
                         key))


ScrapyDB = MongoDB(app.config['MONGODB_STOREDB_NAME'])
ScoreDB = MongoDB(app.config['MONGODB_SCOREDB_NAME'])


def get_begin_day():
    cursor = ScrapyDB.article.find(
        {},
        {'crawl_date': 1}
    ).sort('crawl_date',
           ASCENDING
           ).limit(1)
    return cursor[0]['crawl_date'].date() if cursor.count() else None


def get_end_day():
    cursor = ScrapyDB.article.find(
        {},
        {'crawl_date': 1}
    ).sort('crawl_date',
           DESCENDING
           ).limit(1)
    return cursor[0]['crawl_date'].date() if cursor.count() else None


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
    return {_['id']: _['score'] for _ in cursor}


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
    return {_['id']: _['score'] for _ in cursor}


def get_score(entries):
    spscores = get_spider_score(list({_.spider for _ in entries}))
    ascores = get_article_score(list({_.id for _ in entries}))
    max_spscore = max(spscores.items(),
                      key=lambda i: i[1])[1] if spscores else 1.0
    max_ascore = max(ascores.items(),
                     key=lambda i: i[1])[1] if ascores else 1.0

    def get_score(e):
        return (10.0*spscores.get(e.spider,
                                  0)/max_spscore +
                90.0*ascores.get(e.id,
                                 0)/max_ascore)

    return {_.id: get_score(_) for _ in entries}


def get_entries(day):
    begin = datetime(day.year,
                     day.month,
                     day.day,
                     0,
                     0,
                     0,
                     0)
    end = begin + timedelta(days=1)
    cursor = ScrapyDB.article.find(
        {
            'crawl_date': {'$gte': begin,
                           '$lt': end}
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
    entries_ = [Entry_Day(str(_['_id']),
                _['title'],
                _['category'],
                _['source'],
                _['tag'] if 'tag' in _ else None,
                _['spider'],
                _['domain'],
                _['link'])
                for _ in cursor]
    scores = get_score(entries_)
    entries = defaultdict(list)
    for e in sorted(entries_,
                    key=lambda i: scores[i.id],
                    reverse=True):
        entries[e.category].append(e)
    return entries if entries else None


def get_before_day(day):
    t = datetime(day.year,
                 day.month,
                 day.day,
                 0,
                 0,
                 0,
                 0)
    cursor = ScrapyDB.article.find(
        {
            'crawl_date': {'$lt': t}
        },
        {
            'crawl_date': 1
        }
    ).sort('crawl_date',
           DESCENDING
           ).limit(1)
    return cursor[0]['crawl_date'].date() if cursor.count() else None


def get_after_day(day):
    t = datetime(day.year,
                 day.month,
                 day.day,
                 0,
                 0,
                 0,
                 0)
    nextday = t + timedelta(days=1)
    cursor = ScrapyDB.article.find(
        {
            'crawl_date': {'$gte': nextday}
        },
        {
            'crawl_date': 1
        }
    ).sort('crawl_date',
           ASCENDING
           ).limit(1)
    return cursor[0]['crawl_date'].date() if cursor.count() else None


"""
" spider category
"""


def get_spiders():
    cursor = ScrapyDB.spider.find({},
                                  {'title': 1})
    return {str(_['_id']): _['title'] for _ in cursor}


def get_first_aid(spid):
    cursor = ScrapyDB.article.find(
        {
            'spider': spid
        },
        {
            '_id': 1
        }
    ).sort('_id',
           ASCENDING
           ).limit(1)
    return cursor[0]['_id'] if cursor.count() else None


def get_last_aid(spid):
    cursor = ScrapyDB.article.find(
        {
            'spider': spid
        },
        {
            '_id': 1
        }
    ).sort('_id',
           DESCENDING
           ).limit(1)
    return cursor[0]['_id'] if cursor.count() else None


def get_crawl_date(aid):
    cursor = ScrapyDB.article.find(
        {
            '_id': aid
        },
        {
            'crawl_date': 1
        }
    )
    return cursor[0]['crawl_date'] if cursor.count() else None


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
    ).sort('_id',
           DESCENDING
           ).limit(100)
    return [Entry(str(_['_id']),
                  _['title'])
            for _ in cursor] if cursor.count() else None


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
    ).sort('_id',
           ASCENDING
           ).limit(100)
    return list(reversed([Entry(str(_['_id']),
                                _['title'])
                          for _ in cursor])) if cursor.count() else None


def get_entries_spider(spid):
    cursor = ScrapyDB.article.find(
        {
            'spider': spid
        },
        {
            '_id': 1,
            'title': 1
        }
    ).sort('_id',
           DESCENDING
           ).limit(100)
    return [Entry(str(_['_id']),
                  _['title'])
            for _ in cursor] if cursor.count() else None


Article = namedtuple('Article',
                     ['id',
                      'title',
                      'domain',
                      'link',
                      'content',
                      'lang',
                      'source',
                      'spider'])


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

    if not cursor.count():
        return None

    r = cursor[0]
    if isinstance(r['content'],
                  bytes):
        r['content'] = r['content'].decode('UTF-8')
    if 'source' not in r:
        r['source'] = None
    r['title'] = unescape(r['title'])

    a = Article(r['_id'],
                r['title'],
                r['domain'],
                r['link'],
                r['content'],
                r['lang'],
                r['source'],
                r['spider'])
    return a


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
AID = namedtuple('AID', ['id'])


def get_all_days():
    cursor = ScrapyDB.article.find(
        {},
        {
            'crawl_date': 1
        }
    )
    return {_['crawl_date'].date() for _ in cursor} if cursor.count() else None


def get_all_articles(c):
    cursor = ScrapyDB.article.find(
        {
            'category': c
        },
        {
            '_id': 1
        }
    ).sort('_id',
           ASCENDING)
    return [AID(_['_id']) for _ in cursor] if cursor.count() else None


def get_articles():
    cursor = ScrapyDB.article.find(
        {},
        {
            '_id': 1
        }
    )
    return [_['_id'] for _ in cursor] if cursor.count() else None


def get_max_aid_all():
    pass
