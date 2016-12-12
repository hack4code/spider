# -*- coding: utf-8 -*-


from werkzeug.routing import BaseConverter, ValidationError


class DateConverter(BaseConverter):
    def to_python(self, value):
        from datetime import date
        try:
            return date(*(int(_) for _ in value.split('-')))
        except ValueError:
            raise ValidationError('invalid date format')

    def to_url(self, value):
        return str(value)


class IdConverter(BaseConverter):
    def to_python(self, value):
        from bson.objectid import ObjectId
        from bson.errors import InvalidId
        try:
            return ObjectId(value)
        except InvalidId:
            raise ValidationError('invalid id')

    def to_url(self, value):
        return str(value)
