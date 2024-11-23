# -*- coding: utf-8 -*-


from lxml.html import tostring, HtmlElement
from scrapy.exceptions import DropItem

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
        if isinstance(doc, HtmlElement):
            doc = tostring(
                doc,
                encoding='UTF-8',
                pretty_print=True,
                method='html'
            )
            item['content'] = doc
            item['encoding'] = 'UTF-8'
        if not isinstance(doc, (str, bytes)):
            raise DropItem(
                    f'unknown document type {doc.__class__.__name__}'
            )
        article = dict(item)
        article['lang'] = get_article_lang(item)
        article['spider'] = spider._id
        article['source'] = spider.title
        if not is_exists_article(article):
            save_article(article)
        return item
