# -*- coding: utf-8 -*-


from datetime import date
from flask import render_template, Blueprint

from error import BadRequest
from user import need_uid


entry_page = Blueprint('entry_page',
                       __name__,
                       template_folder='template')


def get_day(day):
    y, m, d = [int(i) for i in day.split('-')]
    return date(y, m, d)


@entry_page.route('/<day>', methods=['GET'])
@need_uid
def show_entries(day):
    try:
        day_entry = get_day(day)
    except:
        raise BadRequest('invalid date {}'.format(day))
    return render_template('day.html',
                           day_entry=day_entry)
