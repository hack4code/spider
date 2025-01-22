# -*- coding: utf-8 -*-


from mydm.spiderfactory import register_spider_meta_cls


class SpiderMeta:
    def __init_subclass__(sub_klass, spider_type, **kwargs):
        super().__init_subclass__(**kwargs)
        register_spider_meta_cls(spider_type, sub_klass)
