# -*- coding: utf-8 -*-


from datetime import date
from flask import render_template, Blueprint, make_response

from error import BadRequest, NotFound
from user import need_uid
from model import get_begin_day, get_end_day, \
    get_entries, get_before_day, get_after_day


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

    day_begin = get_begin_day()
    day_end = get_end_day()

    if day_entry < day_begin or day_entry > date.today():
        raise NotFound('no articles for day {}'.format(day))

    entries = get_entries(day_entry)
    if (len(entries) == 0):
        if day_entry != date.today():
            raise NotFound('no articles for day {}'.format(day_entry))
        else:
            day_entry = get_end_day()
            entries = get_entries(day_entry)
    day_before = get_before_day(day_entry)
    day_after = get_after_day(day_entry)
    link_day_before = '/d/{}'.format(day_before) if day_before else None
    link_day_after = '/d/{}'.format(day_after) if day_after else None
    response = make_response(
        render_template('entries.html',
                        entries=entries,
                        day_entry=str(day_entry),
                        link_day_before=link_day_before,
                        link_day_after=link_day_after)
    )
    if day_entry == day_end:
        response.headers['Cache-Control'] = 'no-cache'
    else:
        response.headers['Cache-Control'] = 'max-age=86400'

    return response
