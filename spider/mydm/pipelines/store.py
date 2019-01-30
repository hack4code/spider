# -*- coding: utf-8 -*-


from lxml.html import tostring, HtmlElement

from ..model import is_exists_article, save_article
from ..ai import get_category


def get_article_lang(item):
    if any(ord(_) > 19967 for _ in item['title']):
        return 'zh'
    return 'en'


class StorePipeline:
    """
        save data to mongodb
    """

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def process_item(self, item, spider):
        if item is not None:
            doc = item['content']
            if not isinstance(doc, (str, bytes)):
                if isinstance(doc, HtmlElement):
                    item['content'] = tostring(
                        doc,
                        encoding='UTF-8',
                        pretty_print=True,
                        method='html'
                    )
                    item['encoding'] = 'UTF-8'
                else:
                    raise Exception((
                        'Error in store pipeline unsupported doc type[{}]'
                        ).format(doc.__class__.__name__))

            item_ = dict(item)
            item_['lang'] = get_article_lang(item)
            item_['spider'] = spider._id
            item_['source'] = spider.title
            item_['category'] = get_category(item_)
            if not is_exists_article(item_):
                save_article(item_)
        return item
