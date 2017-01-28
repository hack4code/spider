# -*- coding: utf-8 -*-


import json
from urllib.parse import urlparse

import pika

from flask import Blueprint, jsonify, request

from app import app


HOST = app.config['BROKER_URL']
CRAWL_KEY = app.config['CRAWL_KEY']
LXMLSPIDER_KEY = app.config['LXMLSPIDER_KEY']
BLOGSPIDER_KEY = app.config['BLOGSPIDER_KEY']

submit_page = Blueprint('submit_page',
                        __name__)


def _send(key, data):
    body = json.dumps(data)
    connection = pika.BlockingConnection(pika.connection.URLParameters(HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_logs',
                             type='direct')
    channel.basic_publish(exchange='direct_logs',
                          routing_key=key,
                          body=body)
    connection.close()


def _check_url(url):
    parser = urlparse(url)
    return False if not parser.scheme or not parser.netloc else True


def _set_removed_xpath_nodes(args):
    removed_xpath_nodes_ = args.get('removed_xpath_nodes')
    if removed_xpath_nodes_:
        removed_xpath_nodes = [_ for _ in (__.strip(' \t\r\n')
                                           for __ in removed_xpath_nodes_)
                               if _]
        if removed_xpath_nodes:
            args['removed_xpath_nodes'] = removed_xpath_nodes


@submit_page.route('/crawl', methods=['POST'])
def crawl():
    spiders = [_ for _ in (__ for __ in request.form['spiders'].split(','))
               if _]
    if not spiders:
        return jsonify(err=1,
                       msg='no spider found')
    _send(CRAWL_KEY,
          {'spiders': spiders})
    return jsonify(err=0)


@submit_page.route('/rss', methods=['POST'])
def gen_atom_spider():
    ATTRS = ('url',
             'category',
             'item_content_xpath',
             'removed_xpath_nodes')

    FORBIDDEN_ATTRS = ('url',
                       'category')

    args = {k.strip(): v.strip()
            for k, v in request.form.items() if k in ATTRS and v}
    if any(_ not in args for _ in FORBIDDEN_ATTRS):
        attrs = [_ for _ in FORBIDDEN_ATTRS if _ not in args]
        return jsonify(err=1,
                       msg='{} field needed'.format(' '.join(attrs)))
    url = args['url']
    if not _check_url(url):
        app.logger.error((
            'Error in gen_atom_spider invalid atom feed url[{}]'
            ).format(url))
        return jsonify(err=2,
                       msg='invalid url')
    _set_removed_xpath_nodes(args)
    _send(LXMLSPIDER_KEY,
          args)
    return jsonify(err=0)


@submit_page.route('/blog', methods=['POST'])
def gen_blog_spider():
    ATTRS = ('url',
             'category',
             'entry_xpath',
             'item_title_xpath',
             'item_link_xpath',
             'item_content_xpath',
             'removed_xpath_nodes')

    FORBIDDEN_ATTRS = ('url',
                       'category',
                       'entry_xpath',
                       'item_title_xpath',
                       'item_link_xpath',
                       'item_content_xpath')

    args = {k.strip(): v.strip()
            for k, v in request.form.items() if k in ATTRS and v}
    _set_removed_xpath_nodes(args)
    if any(_ not in args for _ in FORBIDDEN_ATTRS):
        attrs = [_ for _ in FORBIDDEN_ATTRS if _ not in args]
        return jsonify(err=1,
                       msg='{} field needed'.format(' '.join(attrs)))
    url = args['url']
    if not _check_url(url):
        app.logger.error((
            'Error in gen_blog_spider invalid atom feed url[{}]'
            ).format(url))
        return jsonify(err=2,
                       msg='invalid url')
    _send(BLOGSPIDER_KEY,
          args)
    return jsonify(err=0)
