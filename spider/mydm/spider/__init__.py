# -*- coding: utf-8 -*-


from .html import BLOGSpiderMeta
from .xml import LXMLSpiderMeta
from .spider import ErrbackSpider


SpiderMetaClses = {
        'xml': LXMLSpiderMeta,
        'blog': BLOGSpiderMeta
}


__all__ = [
        'ErrbackSpider',
        'SpiderMetaClses'
]
