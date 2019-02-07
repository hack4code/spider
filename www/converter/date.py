# -*- coding: utf-8 -*-


from datetime import date

from werkzeug.routing import BaseConverter, ValidationError


class DateConverter(BaseConverter):

    def to_python(self, value):
        try:
            return date(*(int(item) for item in value.split('-')))
        except ValueError:
            raise ValidationError('invalid date value')

    def to_url(self, value):
        return str(value)
