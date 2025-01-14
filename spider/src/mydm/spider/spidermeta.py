# -*- coding: utf-8 -*-


class SpiderMeta:
    CLS = {}

    def __init_subclass__(cls, spider_type, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.CLS[spider_type] = cls
