# -*- coding: utf-8 -*-


__all__ = [
    'SpiderFactoryException',
    'ImgException',
    'ContentException'
]


class SpiderFactoryException(Exception):
    """
        exception for spider factory
    """
    pass


class ImgException(Exception):
    """
        exception for image pipeline
    """


class ContentException(Exception):
    """
        exception for content pipeline
    """
