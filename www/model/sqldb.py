# -*- coding: utf-8 -*-


from collections import defaultdict, namedtuple
from datetime import datetime, timedelta
from sqlalchemy import func
from flask.ext.sqlalchemy import SQLAlchemy

from app import app
from util import get_lang


db = SQLAlchemy(app)


class BadAid(Exception):
    pass


class Article(db.Model):
    __tablename__ = app.config['TABLE_NAME']

    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(128))
    title = db.Column(db.String(128))
    category = db.Column(db.String(128))
    data_type = db.Column(db.String(12))
    link = db.Column(db.String(128))
    pub_date = db.Column(db.DateTime)
    crawl_date = db.Column(db.DateTime)
    content = db.Column(db.Text)


def get_begin_day():
    r = db.session.query(
        func.min(Article.crawl_date).label('first')
        ).one()
    return r.first.date()


def get_end_day():
    r = db.session.query(
        func.max(Article.crawl_date).label('end')
        ).one()
    return r.end.date()


def get_entries(day):
    day_s = datetime(day.year, day.month, day.day, 0, 0, 0, 0)
    day_n = day_s + timedelta(days=1)
    articles = Article.query.with_entities(
        Article.title, Article.id, Article.category, Article.pub_date
        ).filter(
            (Article.crawl_date >= day_s) & (Article.crawl_date < day_n)
        ).order_by(Article.pub_date.desc()).all()
    entries = defaultdict(list)
    for a in articles:
        v = {k: getattr(a, k) for k in ('title', 'id', 'pub_date')}
        v['lang'] = get_lang(v['title'])
        entries[a.category].append(v)
    return entries


def get_before_day(day):
    t = datetime(day.year,
                 day.month,
                 day.day,
                 0,
                 0,
                 0,
                 0)
    a = Article.query.with_entities(
        Article.crawl_date
        ).filter(
            Article.crawl_date < t
        ).order_by(
            Article.crawl_date.desc()
        ).first()
    return a.crawl_date.date() if a is not None else None


def get_after_day(day):
    t = datetime(day.year,
                 day.month,
                 day.day,
                 0,
                 0,
                 0,
                 0)
    t_pre = t + timedelta(days=1)
    a = Article.query.with_entities(
        Article.crawl_date
        ).filter(
            Article.crawl_date >= t_pre
        ).order_by(
            Article.crawl_date
        ).first()
    return a.crawl_date.date() if a is not None else None


def get_categories():
    articles = Article.query.with_entities(
        Article.category.distinct().label('category')
    ).all()
    return [a.category for a in articles]


def get_last_aid(category):
    r = db.session.query(
        func.max(Article.id).label('max_aid')
        ).filter_by(category=category).one()
    return r.max_aid


def get_first_aid(category):
    r = db.session.query(
        func.min(Article.id).label('min_aid')
        ).filter_by(category=category).one()
    return r.min_aid


def check_aid(aid, first, last):
    if aid < first or aid > last:
        return False
    return True


def get_entries_next(category, aid):
    entries = Article.query.with_entities(
        Article.id, Article.title
        ).filter(
            (Article.id < aid) & (Article.category == category)
        ).order_by(
            Article.id.desc()
        ).limit(100).all()
    return entries


def get_entries_pre(category, aid):
    entries = Article.query.with_entities(
        Article.id, Article.title
        ).filter(
            (Article.id > aid) & (Article.category == category)
        ).order_by(Article.id).limit(100).all()
    return list(reversed(entries))


def get_entries_category(category):
    entries = Article.query.with_entities(
        Article.id, Article.title
        ).filter_by(
            category=category
        ).order_by(Article.id.desc()).limit(100).all()
    return entries


def format_aid(aid):
    aid = int(aid)
    if aid <= 0:
        raise BadAid()
    return aid


article = namedtuple('Article',
                     ['title', 'domain', 'link', 'content', 'lang'])


def get_article(aid):
    r = Article.query.with_entities(Article.title,
                                    Article.domain,
                                    Article.link,
                                    Article.content
                                    ).filter_by(id=aid).first()
    if r is None:
        return None
    lang = get_lang(r.title)
    a = article(r.title, r.domain, r.link, r.content, lang)
    return a


# function for test
def get_all_days():
    articles = Article.query.with_entities(
        Article.crawl_date
    ).group_by(
        Article.crawl_date
    ) .order_by(
        Article.crawl_date.desc()
    ).all()
    return [a.crawl_date.date() for a in articles]


def get_all_articles(c):
    articles = Article.query.with_entities(
        Article.id
        ).filter_by(
            category=c
        ).order_by(Article.id).all()
    return articles


def get_articles():
    articles = Article.query.with_entities(
        Article.id
        ).all()
    return [a.id for a in articles]


def get_max_aid_all():
    a = Article.query.with_entities(
        Article.id
        ).order_by(
            Article.id.desc()
        ).first()
    return a.id
