# -*- coding: utf-8 -*-


from collections import namedtuple
from flask import request, render_template, Blueprint
from model import get_spiders, get_last_aid, get_first_aid, \
    get_entries_next, get_entries_pre, get_entries_spider, \
    format_aid, check_aid
from error import BadRequest, NotFound


spider_page = Blueprint('spider_page',
                        __name__,
                        template_folder='template')


def check_spider(spid):
    spiders = get_spiders()
    return True if spid in spiders else False


Spider = namedtuple('Spider', ['id', 'source'])


@spider_page.route('/<spid>', methods=['GET'])
def show_category(spid):
    spiders = get_spiders()
    if spid not in spiders:
        raise BadRequest('invalid spider {}'.format(spid))

    aid_last = get_last_aid(spid)
    aid_first = get_first_aid(spid)
    aid = request.args.get('aid', None)
    if aid:
        try:
            aid = format_aid(aid)
        except:
            raise BadRequest('invalid aid {}'.format(aid))

        if not check_aid(aid, aid_first, aid_last):
            raise NotFound('article id {} for {} not existed'.format(
                aid, spid))
        q = request.args.get('q', 'n')
        if q == 'n':
            entries = get_entries_next(spid, aid)
        elif q == 'p':
            entries = get_entries_pre(spid, aid)
    else:
        entries = get_entries_spider(spid)

    if entries is None or len(entries) == 0:
        raise NotFound('no article for {}'.format(spiders[spid]))

    aid_begin = entries[0].id
    aid_end = entries[-1].id
    entry_begin = True if aid_begin == aid_last else False
    entry_end = True if aid_end == aid_first else False
    return render_template('spider.html',
                           spider=Spider(spid, spiders[spid]),
                           entries=entries,
                           aid_begin=aid_begin,
                           aid_end=aid_end,
                           entry_begin=entry_begin,
                           entry_end=entry_end)
