# -*- coding: utf-8 -*-


import logging
import re

from lxml.html import fromstring, HTMLParser, defs
from lxml.html.clean import Cleaner
from lxml.etree import XPathEvalError


logger = logging.getLogger(__name__)


class ContentPipeline(object):
    DEFAULT_ALLOW_CLASSES_NAME = 'allow_classes'
    DEFAULT_REMOVED_CLASSES_NAME = 'removed_classes'
    DEFAULT_REMOVED_XPATH_NODES_NAME = 'removed_xpath_nodes'
    DEFAULT_SAFE_ATTRS = 'safe_attrs'

    SAFE_ATTRS = {'style',
                  'float',
                  'src',
                  'font-size',
                  'font-family',
                  'align'}

    REMOVED_ATTRS = ('class',
                     'id',
                     'width',
                     'height')

    STYLE_REMOVED_ATTRS = (r'width\s*:\s*\d+[^;]*(;|$)',
                           r'height\s*:\s*\d+[^;]*(;|$)')

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
        cls.SAFE_ATTRS_NAME = settings.get(
            'SPIDER_SAFE_ATTRS_NAME',
            cls.DEFAULT_SAFE_ATTRS)
        return cls()

    def format_title(self, title):
        return re.sub(r'(\r|\n|\s)+',
                      ' ',
                      title)

    def make_abs_link(self, doc, link):
        doc.make_links_absolute(link)
        return doc

    def remove_element_with_class(self, doc, removed_classes):
        for e in doc.xpath('//div[@class]'):
            if any(cls in e.get('class').lower() for cls in removed_classes):
                e.drop_tree()
        return doc

    def remove_element_with_xpath(self, doc, removed_xpath_nodes):
        for xpath in filter(lambda x: x.strip(),
                            removed_xpath_nodes):
            try:
                nodes = doc.xpath(xpath)
            except XPathEvalError:
                logger.error((
                    'Error in pipeline content invalid xpath[{}]'
                    ).format(xpath))
            else:
                for _ in nodes:
                    _.drop_tree()
        return doc

    def clean_html(self, doc, allow_classes=None, safe_attrs=None):
        allow_classes = allow_classes or ()
        safe_attrs = (set(defs.safe_attrs) |
                      self.SAFE_ATTRS |
                      set(safe_attrs or []))
        cleaner = Cleaner(safe_attrs_only=True,
                          safe_attrs=safe_attrs)
        doc = cleaner.clean_html(doc)

        while (len(doc) == 1):
            doc = doc[0]

        def rename_tag(doc):
            for e in doc.iter():
                if e.tag.lower() == 'article':
                    e.tag = 'div'

        rename_tag(doc)

        def remove_attr(doc):
            pattern = re.compile('|'.join(self.STYLE_REMOVED_ATTRS),
                                 flags=re.IGNORECASE)
            for e in doc.iter():
                if 'style' in e.attrib:
                    style_ = re.sub(pattern,
                                    '',
                                    e.get('style')).strip()
                    style = re.sub(r'\s{2,}',
                                   ' ',
                                   style_).strip()
                    if style:
                        e.attrib['style'] = style
                    else:
                        e.attrib.pop('style')
                for attr in e.attrib:
                    if (attr in self.REMOVED_ATTRS and
                        not (attr == 'class' and
                             e.get(attr).strip() in allow_classes)):
                        e.attrib.pop(attr)

        remove_attr(doc)

        def remove_tags(doc):
            TAGS = ('//i[not(text())]',
                    '//ins[not(text())]')

            for t in TAGS:
                for e in doc.xpath(t):
                    e.drop_tree()

            for e in doc.xpath('//a/div'):
                e.drop_tree()

            for e in doc.xpath('//div[not(descendant-or-self::div) and '
                               'not(descendant-or-self::img)'):
                text = e.text_content().strip(' \r\n\t')
                if not text:
                    e.drop_tree()

        remove_tags(doc)

        return doc

    def process_item(self, item, spider):
        item['title'] = self.format_title(item['title'])
        doc = item['content']
        if isinstance(doc,
                      (str, bytes)):
            doc = fromstring(bytes(bytearray(doc,
                                             encoding=item['encoding'])),
                             parser=HTMLParser(encoding=item['encoding']))

        # remove element with class name for clean display
        removed_classes = getattr(spider,
                                  self.REMOVED_CLASSES_NAME,
                                  None)
        if removed_classes is not None:
            doc = self.remove_element_with_class(doc,
                                                 removed_classes)

        # remove element with xpath for clean display
        removed_xpath_nodes = getattr(spider,
                                      self.REMOVED_XPATH_NODES_NAME,
                                      None)
        if removed_xpath_nodes is not None:
            doc = self.remove_element_with_xpath(doc,
                                                 removed_xpath_nodes)
        allow_classes = getattr(spider,
                                self.ALLOW_CLASSES_NAME,
                                None)
        safe_attrs = getattr(spider,
                             self.SAFE_ATTRS_NAME,
                             None)
        doc = self.clean_html(doc,
                              allow_classes=allow_classes,
                              safe_attrs=safe_attrs)
        doc = self.make_abs_link(doc,
                                 item['link'])
        item['content'] = doc
        return item
