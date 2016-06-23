# -*- coding: utf-8 -*-


import re


def verify_tags(tags):
    return True if all(len(tag) < 32 for tag in tags) else False


class ReExtractor:
    PATTERN = re.compile(r'>\s*(t|T)ags?\s*:.*<')

    def extract(self, s):
        tags = [tag.strip() for tag in s[s.find(':')+1:-1].split(',')]
        return tags

    def __call__(self, doc):
        matches = re.findall(self.PATTERN, doc)
        if len(matches) == 1:
            stag = matches[0]
            tags = self.extract(stag)
            if verify_tags(tags):
                return tags
        elif len(matches) == 2:
            for stag in matches:
                tags = self.extract(stag)
                if verify_tags(tags):
                    return tags
        elif len(matches) > 2:
            stag = matches[0]
            tags = self.extract(stag)
            if verify_tags(tags):
                return tags
            stag = matches[-1]
            tags = self.extract(stag)
            if verify_tags(tags):
                return tags
        return None


class TagExtractor:
    EXTRACTORS = (ReExtractor,)

    def __call__(self, doc):
        for cls in self.EXTRACTORS:
            tags = cls()(doc)
            if tags is not None:
                return tags
        return None
