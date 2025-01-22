# -*- coding: utf-8 -*-


import mydm.spiderfactory as factory


class SpiderMeta:
    def __init_subclass__(sub_klass, spider_type, **kwargs):
        super().__init_subclass__(**kwargs)
        factory.register_spider_meta_cls(spider_type, sub_klass)
