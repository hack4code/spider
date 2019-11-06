#! /usr/bin/env python


from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from mydm.spiderfactory import SpiderFactory, SpiderFactoryException


settings = get_project_settings()

spider_setting = {
    "_id": "1",
    "category": '新闻',
    "item_content_xpath": '//article',
    "removed_xpath_nodes": [ '//div[@class="article-header"]' ],
    "title": '纽约时报中文网 国际纵览',
    "name": 'CnNytimes',
    "type": 'xml',
    "start_urls": [ 'https://cn.nytimes.com/rss/' ]
}

spider_id = spider_setting['_id']
try:
    cls = SpiderFactory.create_spider(spider_setting)
except SpiderFactoryException as e:
    logger.error('spider create error')

settings['ITEM_PIPELINES'] = {
    'mydm.pipelines.ContentPipeline': 255,
    'mydm.pipelines.ImagesDlownloadPipeline': 300
}

process = CrawlerProcess(settings)
process.crawl(cls)
process.start()
