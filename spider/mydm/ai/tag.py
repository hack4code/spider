# -*- coding: utf-8 -*-


import re

from lxml.html import fromstring, HTMLParser, HtmlElement


class ReExtractor:
    PATTERN = r'(tags?\s*:|Fileds?\s*under\s*:|Tagged\s*with)\s*(?P<tags>.*)'
    FS = ','

    def extract(self, s):
        return [_ for _ in s.split(self.FS) if len(_) < 16]

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
            s = matches[0][1]
            tags = self.extract(s)
            if tags:
                return tags
        elif len(matches) == 2:
            for _, s in matches:
                tags = self.extract(s)
                if tags:
                    return tags
        elif len(matches) > 2:
            s = matches[0][1]
            tags = self.extract(s)
            if tags:
                return tags
            s = matches[-1][1]
            tags = self.extract(s)
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
