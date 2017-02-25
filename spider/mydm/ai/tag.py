# -*- coding: utf-8 -*-


import re

from lxml.html import fromstring, HTMLParser, HtmlElement


class ReExtractor:
    PATTERN = r'(tags?|Filed\s+under)\s*:.*'
    FS = ','

    def extract(self, s):
        tags = [_.strip() for _ in s[s.find(':')+1:-1].split(self.FS)]
        return filter(lambda _: len(_) < 16,
                      tags)

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
        if len(matches) == 1:
            stag = matches[0]
            tags = self.extract(stag)
            if tags:
                return tags
        elif len(matches) == 2:
            for stag in matches:
                tags = self.extract(stag)
                if tags:
                    return tags
        elif len(matches) > 2:
            stag = matches[0]
            tags = self.extract(stag)
            if tags:
                return tags
            stag = matches[-1]
            tags = self.extract(stag)
            if tags:
                return tags


class TagExtractor:
    EXTRACTORS = (ReExtractor,)

    def __call__(self, doc, encoding='UTF-8'):
        for cls in self.EXTRACTORS:
            match = cls()
            tags = match(doc,
                         encoding=encoding)
            return tags


def extract_tags(doc, encoding):
    extract = TagExtractor()
    return extract(doc,
                   encoding=encoding)
