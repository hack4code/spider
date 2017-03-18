# -*- coding: utf-8 -*-


import scrapy


__all__ = [
        'ArticleItem'
]


class ArticleItem(scrapy.Item):
    domain = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    link = scrapy.Field()
    crawl_date = scrapy.Field()
    pub_date = scrapy.Field()
    data_type = scrapy.Field()
    tag = scrapy.Field()
    content = scrapy.Field()
    encoding = scrapy.Field()

    def __repr__(self):
        return u'[{} : {}]'.format(self['title'],
                                   self['link'])
