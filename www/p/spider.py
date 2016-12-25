# -*- coding: utf-8 -*-


from collections import namedtuple
from flask import render_template, Blueprint

from model import get_spiders
from error import BadRequest


spider_page = Blueprint('spider_page',
                        __name__,
                        template_folder='template')


Spider = namedtuple('Spider', ['id', 'source'])


@spider_page.route('/<id:spid>', methods=['GET'])
def show_entries_byspider(spid):
    if spid is None:
        raise BadRequest('invalid spider id')
    spid = str(spid)
    spiders = get_spiders()
    if spid not in spiders:
        raise BadRequest('spider id not existed')
    return render_template('entries.html',
                           spider=Spider(spid,
                                         spiders[spid]))
