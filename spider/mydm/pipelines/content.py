# -*- coding: utf-8 -*-


import logging
import re

from lxml.html import fromstring, tostring, HTMLParser, defs
from lxml.html.clean import Cleaner


logger = logging.getLogger(__name__)


class ContentPipeline(object):
    DEFAULT_ALLOW_CLASSES_NAME = 'allow_classes'
    DEFAULT_REMOVED_CLASSES_NAME = 'removed_classes'
    DEFAULT_REMOVED_XPATH_NODES_NAME = 'removed_xpath_nodes'
    removed_attrs = ('class', 'id')
    safe_attrs = {'style', 'data-url', 'float', 'width', 'height', 'src'}

    @classmethod
    def from_settings(cls, settings):
        cls.ALLOW_CLASSES_NAME = settings.get(
            'SPIDER_ALLOW_CLASSES_NAME',
            cls.DEFAULT_ALLOW_CLASSES_NAME)
        cls.REMOVED_CLASSES_NAME = settings.get(
            'SPIDER_REMOVED_CLASSES_NAME',
            cls.DEFAULT_REMOVED_CLASSES_NAME)
        cls.REMOVED_XPATH_NODES_NAME = settings.get(
            'SPIDER_REMOVED_XPATH_NODES_NAME',
            cls.DEFAULT_REMOVED_XPATH_NODES_NAME)
        return cls()

    def format_title(self, title):
        return re.sub(r'(\r|\n|\s)+', ' ', title)

    def make_abs_link(self, doc, link):
        doc.make_links_absolute(link)
        return doc

    def remove_element_with_class(self, doc, removed_classes):
        for e in doc.xpath('//div[@class]'):
            if any(cls in e.get('class') for cls in removed_classes):
                e.drop_tree()
        return doc

    def remove_element_with_xpath_nodes(self, doc, removed_xpath_nodes):
        for xpath_node in removed_xpath_nodes:
            for e in doc.xpath(xpath_node):
                e.drop_tree()
        return doc

    def clean_html(self, doc, allow_classes):
        allow_classes = () if allow_classes is None else allow_classes
        safe_attrs = set(defs.safe_attrs) | self.safe_attrs
        cleaner = Cleaner(safe_attrs_only=True,
                          safe_attrs=safe_attrs)
        doc = cleaner.clean_html(doc)
        for it in doc.iter():
            if it.tag == 'article':
                it.tag = 'div'
            for attr in self.removed_attrs:
                if attr in it.attrib:
                    if (attr == 'class' and
                            it.get(attr).strip() in allow_classes):
                        continue
                    it.attrib.pop(attr)
        while (len(doc) == 1):
            doc = doc[0]
        for e in doc.xpath('//div'):
            if len(e) == 0:
                e.drop_tree()
        return doc

    def process_item(self, item, spider):
        item['title'] = self.format_title(item['title'])
        try:
            doc = fromstring(bytes(bytearray(item['content'],
                                   encoding=item['encoding'])),
                             parser=HTMLParser(encoding=item['encoding']))
        except TypeError:
            logger.error('{} lxml build doc failed'.format(spider.name))
            return item

        # clean element with class name
        removed_classes = getattr(spider,
                                  self.REMOVED_CLASSES_NAME,
                                  None)
        if removed_classes is not None:
            doc = self.remove_element_with_class(doc, removed_classes)

        # clean element with xpath node
        removed_xpath_nodes = getattr(spider,
                                      self.REMOVED_XPATH_NODES_NAME,
                                      None)
        if removed_xpath_nodes is not None:
            doc = self.remove_element_with_xpath_nodes(doc,
                                                       removed_xpath_nodes)
        # clean html
        allow_classes = getattr(spider,
                                self.ALLOW_CLASSES_NAME,
                                None)
        doc = self.clean_html(doc, allow_classes=allow_classes)
        doc = self.make_abs_link(doc, item['link'])
        item['content'] = tostring(doc, pretty_print=True)
        return item
