# -*- coding: utf-8 -*-


from urllib.parse import urlparse


class cache_property:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        value = self.func(obj)
        setattr(obj, self.func.__name__, value)
        return value


def is_url(value):
    try:
        r = urlparse(value)
    except Exception:
        return False
    else:
        if r.scheme.lower() == 'data' and r.path:
            return True
        else:
            return all([r.scheme, r.netloc, r.path])
