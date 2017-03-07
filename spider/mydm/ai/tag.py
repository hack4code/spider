# -*- coding: utf-8 -*-


import logging
import re

from lxml.html import fromstring, HTMLParser, HtmlElement


logger = logging.getLogger(__name__)


class ReExtractor:
    PATTERN = r'(tags\s*:|Fileds?\s*under\s*:|Tagged\s*with)\s*(.*)'

    def __call__(self, doc, encoding='UTF-8'):
        if isinstance(doc,
                      (str, bytes)):
            doc = fromstring(bytes(bytearray(doc,
                                             encoding=encoding)),
                             parser=HTMLParser(encoding=encoding))
        if not isinstance(doc,
                          HtmlElement):
            return None
        txt = doc.text_content()
        matches = re.findall(self.PATTERN,
                             txt,
                             re.IGNORECASE)

        def extract(s):
            s = re.sub(r'(\s|\t|\r|\n)+',
                       ' ',
                       s)
            tags_ = []
            for _ in s.split(','):
                tag = _.strip()
                if tag:
                    tags_.append(tag)
            tags = []
            for index, tag in enumerate(tags_):
                if index < 2 and len(tag) > 16:
                    return None
                elif len(tag) < 16:
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


class TagExtractor:
    EXTRACTORS = (ReExtractor,)

    def __call__(self, doc, encoding='UTF-8'):
        for cls in self.EXTRACTORS:
            match = cls()
            tags = match(doc,
                         encoding=encoding)
            if tags:
                logger.info('TagExtractor got tags %s',
                            tags)
                return tags


def extract_tags(doc, encoding):
    extract = TagExtractor()
    return extract(doc,
                   encoding=encoding)
