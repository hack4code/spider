# -*- coding: utf-8 -*-


from datetime import date

from werkzeug.routing import BaseConverter, ValidationError


class DateConverter(BaseConverter):

    def to_python(self, value):
        try:
            return date(*(int(_) for _ in value.split('-')))
        except ValueError:
            raise ValidationError('invalid date format')

    def to_url(self, value):
        return str(value)
