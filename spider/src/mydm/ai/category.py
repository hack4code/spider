# -*- coding: utf-8 -*-


from mydm.util import cache_property
from mydm.model import get_category_tags


class CategoryAI():

    @cache_property
    def category_tags(self):
        category_tags = get_category_tags()
        return {
                category: [tag.lower() for tag in tags]
                for category, tags in category_tags.items()
        }

    def category(self, item):
        if 'tag' not in item:
            return item['category']
        for tag in item['tag']:
            lowtag = tag.lower()
            for category, tags in self.category_tags.items():
                if lowtag in tags:
                    return category
        return item['category']


def get_category(item):
    return CategoryAI().category(item)
