# -*- coding: utf-8 -*-


import json

import pika

from flask import Blueprint, jsonify, request

from app import app


HOST = app.config['BROKER_URL']
CRAWL_QUEUE_NAME = app.config['CRAWL_QUEUE_NAME']
LXMLSPIDER_QUEUE_NAME = app.config['LXMLSPIDER_QUEUE_NAME']
BLOGSPIDER_QUEUE_NAME = app.config['BLOGSPIDER_QUEUE_NAME']

feed_page = Blueprint('feed_page',
                      __name__)


def _send(queue, data):
    body = json.dumps(data)
    connection = pika.BlockingConnection(pika.connection.URLParameters(HOST))
    channel = connection.channel()
    channel.queue_declare(queue)
    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=body)


@feed_page.route('/crawl', methods=['POST'])
def crawl():
    spiders = [sp for sp in request.form["spiders"].split(",")]
    _send(CRAWL_QUEUE_NAME,
          {'spiders': spiders})
    return jsonify(err=0)


@feed_page.route('/rss', methods=['POST'])
def gen_atom_spider():
    args = {k.strip(): v.strip() for k, v in request.form.items()}
    if 'url' not in args or 'category' not in args:
        return jsonify(err=1,
                       msg='url or category needed')
    if args['url'] == '':
        return jsonify(err=1,
                       msg='url or category is empty')
    if args['category'] == '':
        args['category'] = u'技术'
    _send(LXMLSPIDER_QUEUE_NAME,
          args)
    return jsonify(err=0)


@feed_page.route("/blog", methods=["POST"])
def gen_blog_spider():
    args = {k.strip(): v.strip() for k, v in request.form.items()}
    if 'url' not in args or 'category' not in args:
        return jsonify(err=1,
                       msg='url or category needed')
    if args['url'] == '' or args['category'] == '':
        return jsonify(err=1,
                       msg='url or category is empty')
    _send(BLOGSPIDER_QUEUE_NAME,
          args)
    return jsonify(err=0)
