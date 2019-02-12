# -*- coding: utf-8 -*-


import uuid
from functools import wraps

from flask import session


def uid():
    return uuid.uuid4().hex


def need_uid(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'uid' not in session:
            session['uid'] = uid()
        return func(*args, **kwargs)
    return wrapper
