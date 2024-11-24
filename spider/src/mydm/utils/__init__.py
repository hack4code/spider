# -*- coding: utf-8 -*-


from .tag import extract_tags
from .head import extract_head
from .tool import cache_property, is_url


__all__ = [
        'extract_tags',
        'extract_head',
        'cache_property',
        'is_url'
]
