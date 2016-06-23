# -*- coding: utf-8 -*-


class HTTPException(Exception):
    def __init__(self, message, payload=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload


class NotFound(HTTPException):
    status_code = 404


class BadRequest(HTTPException):
    status_code = 400
