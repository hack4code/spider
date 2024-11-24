# -*- coding: utf-8 -*-


from typing import TypedDict
from collections import namedtuple
from html import unescape


AID = namedtuple('AID', ['id'])
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
        aid = str(d['_id'])
        content = d.get('content')
        if isinstance(content, bytes):
            content = content.decode('UTF-8')
        title = unescape(d.get('title'))
        return super().__new__(
                cls,
                aid,
                title,
                d.get('domain'),
                d.get('link'),
                d.get('head'),
                content,
                d.get('lang'),
                d.get('source'),
                d.get('spider')
        )


class Spider(TypedDict, total=False):
    id: str
    category: str
    item_content_xpath: str
    removed_xpath_nodes: list[str]
    title: str
    name: str
    type: str
    start_urls: list[str]

    @classmethod
    def from_item(cls, item):
        return cls(
                id = str(item.get('_id')),
                category = item.get('category'),
                item_content_xpath = item.get('item_content_xpath'),
                removed_xpath_nodes = item.get('removed_xpath_nodes'),
                title = item.get('title'),
                name = item.get('name'),
                type = item.get('type'),
                start_urls = item.get('start_urls')
        )
