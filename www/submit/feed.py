# -*- coding: utf-8 -*-


import json

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


@submit_page.route('/crawl', methods=['POST'])
def crawl():
    spiders = [_ for _ in (__ for __ in request.form['spiders'].split(','))
               if _]
    _send(CRAWL_KEY,
          {'spiders': spiders})
    return jsonify(err=0)


@submit_page.route('/rss', methods=['POST'])
def gen_atom_spider():
    args = {k.strip(): v.strip() for k, v in request.form.items()}
    if not args.get('url') or not args.get('category'):
        return jsonify(err=1,
                       msg='url or category needed')
    _send(LXMLSPIDER_KEY,
          args)
    return jsonify(err=0)


@submit_page.route("/blog", methods=["POST"])
def gen_blog_spider():
    args = {k.strip(): v.strip() for k, v in request.form.items()}
    if not args.get('url') or not args.get('category'):
        return jsonify(err=1,
                       msg='url or category needed')
    _send(BLOGSPIDER_KEY,
          args)
    return jsonify(err=0)
