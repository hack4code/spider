# -*- coding: utf-8 -*-


from collections import namedtuple
from flask import render_template, Blueprint

from model import get_spiders
from error import BadRequest


spider_page = Blueprint('spider_page',
                        __name__,
                        template_folder='template')


def check_spider(spid):
    spiders = get_spiders()
    return True if spid in spiders else False


Spider = namedtuple('Spider', ['id', 'source'])


@spider_page.route('/<spid>', methods=['GET'])
def sp_entries(spid):
    spiders = get_spiders()
    if spid not in spiders:
        raise BadRequest('invalid spider id')
    return render_template('spentries.html',
                           spider=Spider(spid, spiders[spid]))
