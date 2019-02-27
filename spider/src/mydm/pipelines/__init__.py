# -*- coding: utf-8 -*-


from .store import StorePipeline
from .content import ContentPipeline
from .image import ImagesDlownloadPipeline


__all__ = [
        'ContentPipeline',
        'ImagesDlownloadPipeline',
        'StorePipeline'
]
