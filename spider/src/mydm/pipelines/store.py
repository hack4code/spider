# -*- coding: utf-8 -*-


from lxml.html import tostring, HtmlElement

from scrapy.exceptions import DropItem

from mydm.ai import get_category
from mydm.model import is_exists_article, save_article


def get_article_lang(item):
    if any(ord(cha) > 19967 for cha in item['title']):
        return 'zh'
    return 'en'


class StorePipeline:

    @classmethod
    def from_crawler(cls, crawler):
        pipe = cls()
        pipe.crawler = crawler
        return pipe

    def process_item(self, item, spider):
        doc = item['content']
        if not isinstance(doc, (str, bytes)):
            if not isinstance(doc, HtmlElement):
                raise DropItem(
                        f'unknown document type {doc.__class__.__name__}'
                )
            item['content'] = tostring(
                doc,
                encoding='UTF-8',
                pretty_print=True,
                method='html'
            )
            item['encoding'] = 'UTF-8'

        itemd = dict(item)
        itemd['lang'] = get_article_lang(item)
        itemd['spider'] = spider._id
        itemd['source'] = spider.title
        itemd['category'] = get_category(itemd)
        if not is_exists_article(itemd):
            save_article(itemd)
        return item
