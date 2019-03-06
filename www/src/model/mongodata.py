# -*- coding: utf-8 -*-


from html import unescape
from collections import namedtuple


AID = namedtuple('AID', ['id'])
Spider = namedtuple('Spider', ['id', 'source'])
EntryBase = namedtuple('Entry', ['id', 'title'])


class Entry(EntryBase):

    def __new__(cls, d):
        return super().__new__(
                cls,
                str(d['_id']),
                d.get('title')
        )


EntryDayBase = namedtuple(
        'EntryDay',
        ['id',
         'title',
         'category',
         'source',
         'tag',
         'spider',
         'domain',
         'link']
)


class EntryDay(EntryDayBase):

    def __new__(cls, d):
        return super().__new__(
                cls,
                str(d['_id']),
                d.get('title'),
                d.get('category'),
                d.get('source'),
                d.get('tag'),
                d.get('spider'),
                d.get('domain'),
                d.get('link')
        )


ArticleBase = namedtuple(
        'Article',
        ['id',
         'title',
         'domain',
         'link',
         'head',
         'content',
         'lang',
         'source',
         'spider']
)


class Article(ArticleBase):

    def __new__(cls, d):
        content = d.get('content')
        if isinstance(content, bytes):
            content = content.decode('UTF-8')
        title = unescape(d.get('title'))
        return super().__new__(
                cls,
                str(d['_id']),
                title,
                d.get('domain'),
                d.get('link'),
                d.get('head'),
                content,
                d.get('lang'),
                d.get('source'),
                d.get('spider')
        )
