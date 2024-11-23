# -*- coding: utf-8 -*-


import re

from lxml.etree import ParserError
from lxml.html import fromstring, HTMLParser, HtmlElement


class ReExtractor:

    p = re.compile(
            r'(tags\s*:|Fileds?\s*under\s*:|Tagged\s*with)\s*(.*)',
            re.IGNORECASE
    )

    def __call__(self, doc):
        matches = self.p.findall(doc.text_content())

        def extract(s):
            s = re.sub(r'(\s|\t|\r|\n)+', ' ', s)
            tags = []
            for item in s.split(','):
                tag = item.strip()
                if tag:
                    tags.append(tag)
            return tags

        if len(matches) == 1:
            s = matches[0][1]
            tags = extract(s)
            if tags:
                return tags
        elif len(matches) == 2:
            for _, s in matches:
                tags = extract(s)
                if tags:
                    return tags
        elif len(matches) > 2:
            s = matches[0][1]
            tags = extract(s)
            if tags:
                return tags
            s = matches[-1][1]
            tags = extract(s)
            if tags:
                return tags


class LXMLExtractor:

    p = re.compile(
            r'^\s*(tags\s*:|Fileds?\s*under\s*:|Tagged\s*with)\s*$',
            re.IGNORECASE
    )

    def __call__(self, doc):
        for e in doc.xpath('//*[count(child::*)=0]'):
            if self.p.match(e.text_content()) is not None:
                container = e.getparent()
                for idx, item in enumerate(container):
                    if item is e:
                        break
                tags = []
                for item in container[idx+1:]:
                    tag = item.text_content().strip(',\r\n\t ')
                    if tag:
                        tags.append(tag)
                return tags


class TagExtractor:

    EXTRACTORS = (ReExtractor, LXMLExtractor)

    def __call__(self, doc, encoding='UTF-8'):
        if isinstance(doc, (str, bytes)):
            try:
                doc = fromstring(
                        bytes(bytearray(doc, encoding=encoding)),
                        parser=HTMLParser(encoding=encoding)
                )
            except ParserError:
                return
        if not isinstance(doc, HtmlElement):
            return
        for cls in self.EXTRACTORS:
            ext_tags = cls()(doc)
            if ext_tags:
                tags = []
                for idx, tag in enumerate(ext_tags):
                    if idx < 2 and len(tag) > 16:
                        break
                    elif len(tag) < 16:
                        tags.append(tag)
                else:
                    return tags


def extract_tags(doc, encoding):
    return TagExtractor()(doc, encoding=encoding)
