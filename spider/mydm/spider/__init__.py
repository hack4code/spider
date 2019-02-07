# -*- coding: utf-8 -*-


from .xml import LXMLSpiderMeta
from .html import BLOGSpiderMeta
from .spider import ErrbackSpider


SpiderMetaClses = {
    'xml': LXMLSpiderMeta,
    'blog': BLOGSpiderMeta
}


__all__ = [
    'ErrbackSpider',
    'SpiderMetaClses'
]
