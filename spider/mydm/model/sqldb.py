# -*- coding: utf-8 -*-


from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, \
    Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import Index

from scrapy.utils.project import get_project_settings


settings = get_project_settings()
Base = declarative_base()


class Article(Base):
    __tablename__ = settings['TABLE_NAME']

    id = Column(Integer, primary_key=True)
    domain = Column(String(128))
    title = Column(String(128))
    category = Column(String(128))
    data_type = Column(String(12))
    link = Column(String(128))
    pub_date = Column(DateTime)
    crawl_date = Column(DateTime)
    content = Column(Text)

    __table_args__ = (Index('crawl_date_idx', 'crawl_date'),
                      Index('domain_title_pub_date_idx',
                            'domain', 'title', 'pub_date'))

    def __repr__(self):
        return u'<Article(title={}[category={}])>'.format(self.title,
                                                          self.category)


class Feed(Base):
    __tablename__ = settings['FEED_TABLE_NAME']

    id = Column(Integer, primary_key=True)
    url = Column(String(128))
    create_date = Column(DateTime)
    __table_args__ = (Index('url_idx', 'url'),)

    def __repr__(self):
        return '<Feed(url:{}>'.format(self.url)


class SqlDB(object):

    def __init__(self):
        engine = create_engine(settings['DB_NAME'])
        Base.metadata.tables[settings['TABLE_NAME']].create(
            bind=engine, checkfirst=True)
        Base.metadata.tables[settings['FEED_TABLE_NAME']].create(
            bind=engine, checkfirst=True)
        self.session = sessionmaker(engine)()

    def is_exists_feed(self, url):
        return self.session.query(exists().where(Feed.url == url)).scalar()

    def save_feed(self, url):
        feed = Feed(url=url, create_date=datetime.now())
        self.session.add(feed)
        self.session.commit()

    def is_exists_article(self, item):
        q = self.session.query(
            Article
        ).filter(
            (Article.domain == item['domain']) &
            (Article.title == item['title']) &
            (Article.pub_date >= item['pub_date'])).exists()
        return self.session.query(q).scalar()

    def save_article(self, item):
        article = Article(domain=item['domain'],
                          title=item['title'],
                          category=item['category'],
                          data_type=item['data_type'],
                          link=item['link'],
                          pub_date=item['pub_date'],
                          crawl_date=item['crawl_date'],
                          content=item['content'])
        self.session.add(article)
        self.session.commit()
