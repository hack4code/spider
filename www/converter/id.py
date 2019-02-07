# -*- coding: utf-8 -*-


from bson.errors import InvalidId
from bson.objectid import ObjectId
from werkzeug.routing import BaseConverter, ValidationError


class IdConverter(BaseConverter):

    def to_python(self, value):
        try:
            return ObjectId(value)
        except InvalidId:
            raise ValidationError('invalid ID value')

    def to_url(self, value):
        return str(value)
