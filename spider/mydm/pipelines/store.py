# -*- coding: utf-8 -*-


from ..model import is_exists_article, save_article
from ..ai import get_category


def get_article_lang(item):
    if any(ord(c) > 19967 for c in item['title']):
        return 'zh'
    return 'en'


class StorePipeline(object):
    """
        save content to mongodb
    """

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def process_item(self, item, spider):
        doc = item['content']
        if item is not None:
            if not (isinstance(doc, str) or isinstance(doc, bytes)):
                from lxml.html import tostring
                item['content'] = tostring(doc,
                                           encoding='UTF-8',
                                           pretty_print=True,
                                           method='html')
                item['encoding'] = 'UTF-8'

            item_ = dict(item)
            item_['lang'] = get_article_lang(item)
            item_['spider'] = spider._id
            item_['source'] = spider.title
            item_['category'] = get_category(item_)
            if not is_exists_article(item_):
                save_article(item_)
        return item
