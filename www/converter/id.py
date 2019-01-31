# -*- coding: utf-8 -*-


from werkzeug.routing import BaseConverter, ValidationError
from bson.objectid import ObjectId
from bson.errors import InvalidId


class IdConverter(BaseConverter):

    def to_python(self, value):
        try:
            return ObjectId(value)
        except InvalidId:
            raise ValidationError('invalid id')

    def to_url(self, value):
        return str(value)
