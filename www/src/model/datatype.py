# -*- coding: utf-8 -*-


from typing import TypedDict
from html import unescape


class Entry(TypedDict, total=False):
    id: str
    title: str

    @classmethod
    def from_item(cls, item):
        aid = str(item.get('_id'))
        return cls(
            id = aid,
            title = item.get('title')
        )


class EntryDay(TypedDict, total=False):
    id: str
    title: str
    category: str
    source: str
    tag: list[str] | None
    spider: str
    domain: str
    link: str

    @classmethod
    def from_item(cls, item):
        aid = str(item.get('_id'))
        spider = str(item.get('spider'))
        return cls(
                id = aid,
                spider = spider,
                title = item.get('title'),
                category = item.get('category'),
                source = item.get('source'),
                tag = item.get('tag'),
                domain = item.get('domain'),
                link = item.get('link')
        )


class Article(TypedDict, total=False):
    id: str
    title: str
    domain: str
    link: str
    head: str
    content: str
    lang: str
    source: str
    spider: str

    @classmethod
    def from_item(cls, item):
        aid = str(item.get('_id'))
        title = unescape(item.get('title'))
        content = item.get('content')
        if isinstance(content, bytes):
            content = content.decode('UTF-8')
        return cls(
            id = aid,
            title = title,
            content = content,
            domain = item.get('domain'),
            link = item.get('link'),
            lang = item.get('lang'),
            source = item.get('source'),
            spider = item.get('spider')
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
    css: str

    @classmethod
    def from_item(cls, item):
        return cls(
            id = str(item.get('_id')),
            category = item.get('category'),
            title = item.get('title'),
            start_urls = item.get('start_urls'),
            name = item.get('name'),
            type = item.get('type'),
            css = item.get('css', ""),
            item_content_xpath = item.get('item_content_xpath', ""),
            removed_xpath_nodes = item.get('removed_xpath_nodes', []),
        )
