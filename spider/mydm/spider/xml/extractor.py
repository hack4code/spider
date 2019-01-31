# -*- coding: utf-8 -*-


from html import unescape
from urllib.parse import urlparse

from zope.interface import Interface, implementer
from dateutil.parser import parse as get_date
from lxml.etree import QName


def is_url(v):
    try:
        r = urlparse(v)
    except Exception:
        return False
    else:
        return all([r.scheme, r.netloc, r.path])


class ITagExtractor(Interface):
    def match(self, e):
        """ check if the element  match the tag """

    def extract(self, e):
        """ extract data from element """


@implementer(ITagExtractor)
class TitleTag:
    tag = 'title'

    def __init__(self):
        self.val = None

    def match(self, e):
        name = QName(e.tag).localname.lower()
        return name == 'title'

    def extract(self, e):
        v = e.text
        if v is not None:
            v = v.strip('\r\t\n ')
        if v:
            self.val = unescape(v)


@implementer(ITagExtractor)
class LinkTag:
    tag = 'link'

    def __init__(self):
        self.val = None

    def match(self, e):
        name = QName(e.tag).localname.lower()
        return name in ('link', 'guid')

    def extract(self, e):
        if 'href' in e.attrib:
            v = e.attrib['href']
        else:
            v = e.text
        if v is not None:
            v = v.strip('\r\t\n ')
        if not v:
            return
        if not is_url(v):
            return
        if self.val is None:
            self.val = v
        elif 'isPermaLink' in e.attrib:
            self.val = v


@implementer(ITagExtractor)
class PubDateTag:
    tag = 'pub_date'

    def __init__(self):
        self.val = None

    def match(self, e):
        name = QName(e.tag).localname.lower()
        return name in ('pubdate', 'updated')

    def extract(self, e):
        if e.text is None:
            return
        v = get_date(e.text, ignoretz=True)
        if self.val is None or self.val < v:
            self.val = v


@implementer(ITagExtractor)
class CategoryTag:
    tag = 'tag'
    attrs = ['term', ]

    def __init__(self):
        self.val = None

    def match(self, e):
        name = QName(e.tag).localname.lower()
        return name == 'category'

    def extract(self, e):
        v = None
        if e.text is None and e.attrib:
            for _, d in e.attrib.items():
                if d is not None and len(d) > 0:
                    v = d
                    break
        else:
            v = e.text
        if v is None:
            return
        if self.val is None:
            self.val = []
        self.val.append(v.strip('\t\n '))


@implementer(ITagExtractor)
class ContentTag:
    tag = 'content'

    def __init__(self):
        self.val = None

    def match(self, e):
        name = QName(e.tag).localname.lower()
        return name in ('encoded', 'description', 'content', 'summary')

    def extract(self, e):
        if e.text is None:
            return
        if self.val is None or len(self.val) < len(e.text):
            self.val = e.text


class ItemExtractor:
    def __init__(self):
        self.extractors = [
                TitleTag(),
                LinkTag(),
                PubDateTag(),
                CategoryTag(),
                ContentTag()
        ]

    def __call__(self, entry):
        for e in entry:
            for ext in self.extractors:
                try:
                    if ext.match(e):
                        ext.extract(e)
                        break
                except ValueError:
                    continue
        return {
                item.tag: item.val
                for item in self.extractors
                if item.val is not None
        }
