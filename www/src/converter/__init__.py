# -*- coding: utf-8 -*-


from .date import DateConverter
from .id import IdConverter


__all__ = ['init_converter']


def init_converter(app):
    app.url_map.converters['date'] = DateConverter
    app.url_map.converters['id'] = IdConverter
