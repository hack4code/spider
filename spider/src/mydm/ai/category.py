# -*- coding: utf-8 -*-


from mydm.model import get_category_tags
from mydm.util import cache_property


class CategoryAI():

    @cache_property
    def tags(self):
        tags = get_category_tags()
        return {c: [_.lower() for _ in t] for c, t in tags.items()}

    def category(self, item):
        if 'tag' not in item:
            return item['category']
        for tag in item['tag']:
            lowtag = tag.lower()
            for c, t in self.tags.items():
                if lowtag in t:
                    return c
        return item['category']


ai = CategoryAI()


def get_category(item):
    return ai.category(item)
