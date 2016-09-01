# -*- coding: utf-8 -*-


from datetime import date
from flask import render_template, Blueprint

from error import BadRequest
from user import need_uid


entry_page = Blueprint('entry_page',
                       __name__,
                       template_folder='template')


@entry_page.route('/<day>', methods=['GET'])
@need_uid
def show_entries(day):
    try:
        y, m, d = [int(i) for i in day.split('-')]
        day_entry = date(y, m, d)
    except:
        raise BadRequest('invalid day')

    return render_template('day.html',
                           day_entry=day_entry)
