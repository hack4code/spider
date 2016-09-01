# -*- coding: utf-8 -*-


from collections import namedtuple, defaultdict
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from app import app


Entry = namedtuple('Entry', ['id', 'title'])
Entry_Day = namedtuple('Entry_Day', ['id',
                                     'title',
                                     'category',
                                     'source',
                                     'tag',
                                     'spider',
                                     'domain',
                                     'link'])


class MongoDB():
    def __init__(self, name):
        self.name = name
        self.client = MongoClient(app.config['MONGODB_URI'],
                                  connect=False)
        self.db = None

    def connect(self):
        db = self.client[self.name]
        db.authenticate(app.config['MONGODB_USER'],
                        app.config['MONGODB_PWD'])
        self.db = db

    def __getattr__(self, key):
        if self.db is None:
            self.connect()
        try:
            return self.db[key]
        except KeyError:
            raise AttributeError(
                '{} db has no collection {}'.format(self.name, key))


articledb = MongoDB(app.config['MONGODB_STOREDB_NAME'])
scoredb = MongoDB(app.config['MONGODB_SCOREDB_NAME'])


def get_begin_day():
    cursor = articledb.article.find(
        {},
        {'crawl_date': 1}
    ).sort('crawl_date', ASCENDING).limit(1)
    return cursor[0]['crawl_date'].date() if cursor.count() > 0 else None


def get_end_day():
    cursor = articledb.article.find(
        {},
        {'crawl_date': 1}
    ).sort('crawl_date', DESCENDING).limit(1)
    return cursor[0]['crawl_date'].date() if cursor.count() > 0 else None


def get_spider_score(spids):
    cursor = scoredb.spider.find(
        {
            'id': {'$in': spids}
        },
        {
            'id': 1,
            'score': 1
        }
    )
    return {r['id']: r['score'] for r in cursor}


def get_article_score(aids):
    cursor = scoredb.article.find(
        {
            'id': {'$in': aids}
        },
        {
            'id': 1,
            'score': 1
        }
    )
    return {r['id']: r['score'] for r in cursor}


def get_score(el):
    spids = set()
    aids = set()
    for e in el:
        spids.add(e.spider)
        aids.add(e.id)
    sp_scores = get_spider_score(list(spids))
    a_scores = get_article_score(list(aids))
    max_sp_score = max(sp_scores.items(),
                       key=lambda i: i[1])[1] if len(sp_scores) > 0 else 1.0
    max_a_score = max(a_scores.items(),
                      key=lambda i: i[1])[1] if len(a_scores) > 0 else 1.0
    scores = {}
    for e in el:
        spid = e.spider
        aid = e.id
        sp_score = sp_scores[spid] if spid in sp_scores else 0
        a_score = a_scores[aid] if aid in a_scores else 0
        score = 10.0*sp_score/max_sp_score + 90.0*a_score/max_a_score
        scores[aid] = score
    return scores


def get_entries(day):
    day_s = datetime(day.year, day.month, day.day, 0, 0, 0, 0)
    day_n = day_s + timedelta(days=1)
    cursor = articledb.article.find(
        {
            'crawl_date': {'$gte': day_s,
                           '$lt': day_n}
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
    el = [Entry_Day(str(r['_id']),
                    r['title'],
                    r['category'],
                    r['source'],
                    r['tag'] if 'tag' in r else None,
                    r['spider'],
                    r['domain'],
                    r['link'])
          for r in cursor]
    scores = get_score(el)
    entries = defaultdict(list)
    for e in sorted(el, key=lambda i: scores[i.id], reverse=True):
        entries[e.category].append(e)
    return entries


def get_before_day(day):
    t = datetime(day.year,
                 day.month,
                 day.day,
                 0,
                 0,
                 0,
                 0)
    cursor = articledb.article.find(
        {
            'crawl_date': {'$lt': t}
        },
        {
            'crawl_date': 1
        }
    ).sort('crawl_date', DESCENDING).limit(1)
    return None if cursor.count() == 0 else cursor[0]['crawl_date'].date()


def get_after_day(day):
    t = datetime(day.year,
                 day.month,
                 day.day,
                 0,
                 0,
                 0,
                 0)
    t_pre = t + timedelta(days=1)
    cursor = articledb.article.find(
        {
            'crawl_date': {'$gte': t_pre}
        },
        {
            'crawl_date': 1
        }
    ).sort('crawl_date', ASCENDING).limit(1)
    return None if cursor.count() == 0 else cursor[0]['crawl_date'].date()


"""
" spider category
"""


def get_spiders():
    cursor = articledb.spider.find({}, {'title': 1})
    return {str(r['_id']): r['title'] for r in cursor}


def get_first_aid(spid):
    cursor = articledb.article.find(
        {
            'spider': spid
        },
        {
            '_id': 1
        }
    ).sort('_id', ASCENDING).limit(1)
    return None if cursor.count() == 0 else cursor[0]['_id']


def get_last_aid(spid):
    cursor = articledb.article.find(
        {
            'spider': spid
        },
        {
            '_id': 1
        }
    ).sort('_id', DESCENDING).limit(1)
    return None if cursor.count() == 0 else cursor[0]['_id']


def check_aid(aid, first, last):
    if aid < first or aid > last:
        return False
    return True


def get_crawl_date(aid):
    cursor = articledb.article.find(
        {
            '_id': aid
        },
        {
            'crawl_date': 1
        }
    )
    return None if cursor.count() == 0 else cursor[0]['crawl_date']


def get_entries_next(spid, aid):
    cursor = articledb.article.find(
        {
            '_id': {'$lt': aid},
            'spider': spid
        },
        {
            '_id': 1,
            'title': 1
        }
    ).sort('_id', DESCENDING).limit(100)
    if cursor.count() == 0:
        return None
    entries = []
    for a in cursor:
        entries.append(Entry(a['_id'], a['title']))
    return entries


def get_entries_pre(spid, aid):
    cursor = articledb.article.find(
        {
            '_id': {'$gt': aid},
            'spider': spid
        },
        {
            '_id': 1,
            'title': 1
        }
    ).sort('_id', ASCENDING).limit(100)
    if cursor.count() == 0:
        return None
    entries = []
    for a in cursor:
        entries.append(Entry(a['_id'], a['title']))
    return list(reversed(entries))


def get_entries_spider(spid):
    cursor = articledb.article.find(
        {
            'spider': spid
        },
        {
            '_id': 1,
            'title': 1
        }
    ).sort('_id', DESCENDING).limit(100)
    if cursor.count() == 0:
        return None
    entries = []
    for a in cursor:
        entries.append(Entry(a['_id'], a['title']))
    return entries


def format_aid(aid):
    return ObjectId(aid)


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
    cursor = articledb.article.find(
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
    )
    if cursor.count() == 0:
        return None
    r = cursor[0]
    a = Article(r['_id'],
                r['title'],
                r['domain'],
                r['link'],
                r['content'],
                r['lang'],
                r['source'] if 'source' in r else None,
                r['spider'])
    return a


def vote_article(a):
    scoredb.article.update(
        {
            'id': a.id
        },
        {
            '$inc': {'score': 1}
        },
        upsert=True
    )
    scoredb.spider.update(
        {
            'id': a.spider
        },
        {
            '$inc': {'score': 1}
        },
        upsert=True
    )


def get_categories():
    return articledb.article.distinct('category')


# function for test
Aid = namedtuple('Aid', ['id'])


def get_all_days():
    cursor = articledb.article.find(
        {},
        {
            'crawl_date': 1
        }
    )
    return None if cursor.count() == 0 else set(
        [r['crawl_date'].date() for r in cursor])


def get_all_articles(c):
    cursor = articledb.article.find(
        {
            'category': c
        },
        {
            '_id': 1
        }
    ).sort('_id', ASCENDING)
    return None if cursor.count() == 0 else [Aid(r['_id']) for r in cursor]


def get_articles():
    cursor = articledb.article.find(
        {},
        {
            '_id': 1
        }
    )
    return None if cursor.count() == 0 else [r['_id'] for r in cursor]


def get_max_aid_all():
    pass
