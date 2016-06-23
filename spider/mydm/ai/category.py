# -*- coding: utf-8 -*-


from ..model import get_category_tags


class CategoryAI():

    def __init__(self):
        tags = get_category_tags()
        self.tags = {c: [t.lower() for t in a] for c, a in tags.items()}

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
