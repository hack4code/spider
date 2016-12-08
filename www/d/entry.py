# -*- coding: utf-8 -*-


from flask import render_template, Blueprint

from error import BadRequest
from user import need_uid


entry_page = Blueprint('entry_page',
                       __name__,
                       template_folder='template')


@entry_page.route('/<date:day>', methods=['GET'])
@need_uid
def show_entries(day):
    if day is None:
        raise BadRequest('invalid day')
    return render_template('day.html',
                           day_entry=day)
