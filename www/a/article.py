# -*- coding: utf-8 -*-


import os
from flask import render_template, Blueprint
from model import get_article
from error import NotFound, BadRequest

article_page = Blueprint('article_page',
                         __name__,
                         template_folder='template',
                         static_folder='../static')


def get_css(dom):
    path = '{}/css/{}.css'.format(article_page.static_folder,
                                  dom)
    return '{}.css'.format(dom) if os.path.isfile(path) else None


@article_page.route('/<id:aid>', methods=['GET'])
def show_article(aid):
    if aid is None:
        raise BadRequest('invalid article id')

    a = get_article(aid)
    if a is None:
        raise NotFound('article for id={} not exist'.format(aid))

    return render_template('article.html',
                           article=a,
                           dom_css=get_css(a.domain))
