# -*- coding: utf-8 -*-


import logging
import sys
import time
import json
from multiprocessing import Process

import pika

from scrapy.utils.project import get_project_settings

from task import crawl, gen_lxmlspider, gen_blogspider


settings = get_project_settings()


def cron(ch, method, properties, body):
    logger = logging.getLogger(__name__)
    args = json.loads(body)
    p = Process(target=crawl,
                args=(args,))
    logger.info('cron task starting ...')
    p.daemon = True
    p.start()
    p.join()
    logger.info('cron task finished')


def lxmlspider(ch, method, properties, body):
    args = json.loads(body)
    gen_lxmlspider(args)


def blogspider(ch, method, properties, body):
    args = json.loads(body)
    gen_blogspider(args)


def task(callback, key):
    url = '{}?heartbeat=0'.format(settings['BROKER_URL'])
    connection = pika.BlockingConnection(pika.connection.URLParameters(url))
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_logs',
                             type='direct')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=key)
    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)
    channel.start_consuming()


def init_logger(settings):
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(settings['LOG_LEVEL'])
    handler.setFormatter(logging.Formatter(settings['LOG_FORMAT'],
                                           settings['LOG_DATEFORMAT']))
    root.addHandler(handler)


def main():
    init_logger(settings)
    logger = logging.getLogger(__name__)
    TASKS = [(cron, settings['CRAWL_KEY']),
             (lxmlspider, settings['LXMLSPIDER_KEY']),
             (blogspider, settings['BLOGSPIDER_KEY'])]
    consumers = [(Process(target=task,
                          args=_),
                  _) for _ in TASKS]
    time.sleep(60)
    for p, _ in consumers:
        p.start()
    logger.info('rpc task running ...')
    while True:
        for i, (p, args) in enumerate(consumers):
            logger.info('check task state ...')
            if not p.is_alive():
                logger.error((
                    'function {} got exception'
                    ).format(TASKS[i][0].__name__))
                p.join()
                np = Process(target=task,
                             args=args)
                np.start()
                consumers[i] = (np, args)
            time.sleep(120)


if __name__ == '__main__':
    main()
