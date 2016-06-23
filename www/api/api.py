# -*- coding: utf-8 -*-


import logging
import requests
from flask import Blueprint, jsonify, request, session

from app import app
from model import format_aid, get_article, vote_article

logger = logging.getLogger(__name__)


api_page = Blueprint('api_page',
                     __name__,
                     template_folder='template')


@api_page.route('/feed/atom', methods=['POST'])
def gen_atom_feed():
    try:
        url = '{}/atom'.format(app.config['FEED_SUBMIT_URL'])
        r = requests.post(url, request.form)
    except:
        logger.error('genspider[atom] error')
        return jsonify(err=1, msg='exception')
    rj = r.json()
    return jsonify(err=rj['err'], msg=rj['msg'])


@api_page.route('/feed/blog', methods=['POST'])
def gen_blog_feed():
    try:
        url = '{}/blog'.format(app.config['FEED_SUBMIT_URL'])
        r = requests.post(url, request.form)
    except:
        logger.error('genspider[blog] error')
        return jsonify(err=1, msg='exception')
    rj = r.json()
    return jsonify(err=rj['err'], msg=rj['msg'])


@api_page.route('/vote', methods=['POST'])
def vote():
    if 'uid' not in session:
        return jsonify(err=1, msg='no uid')
    if 'aid' not in request.form:
        return jsonify(err=2, msg='no aid')
    aid = request.form['aid']
    try:
        aid = format_aid(aid)
    except:
        return jsonify(err=3, msg='invalid aid')
    a = get_article(aid)
    if a is None:
        return jsonify(err=4, msg='no article')
    vote_article(a)
    return jsonify(err=0, aid=str(aid))
