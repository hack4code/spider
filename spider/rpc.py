# -*- coding: utf-8 -*-


import logging
import sys
from time import sleep
import json
from multiprocessing import Process

import pika

from scrapy.utils.project import get_project_settings

from task import crawl, gen_lxmlspider, gen_blogspider


settings = get_project_settings()


def task(callback, key):
    consumers = []
    url = '{}?heartbeat=600'.format(settings['BROKER_URL'])
    connection = pika.BlockingConnection(pika.connection.URLParameters(url))
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_logs',
                             type='direct')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=key)

    def consume(ch, method, properties, body):
        args = json.loads(body)
        p = Process(target=callback,
                    args=(args,))
        p.daemon = True
        p.start()
        consumers.append(p)

    channel.basic_consume(consume,
                          queue=queue_name,
                          no_ack=True)
    while True:
        connection.process_data_events()
        if any(not _.is_alive() for _ in consumers):
            consumers_ = []
            for _ in consumers:
                if _.is_alive():
                    consumers_.append(_)
                else:
                    _.join()
            consumers = consumers_
        sleep(60)


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
    TASKS = [(crawl, settings['CRAWL_KEY']),
             (gen_lxmlspider, settings['LXMLSPIDER_KEY']),
             (gen_blogspider, settings['BLOGSPIDER_KEY'])]
    tasks = [(Process(target=task,
                      args=_),
              _) for _ in TASKS]
    sleep(10)
    for p, _ in tasks:
        p.start()
    logger.info('rpc task running ...')
    while True:
        for i, (p, args) in enumerate(tasks):
            if not p.is_alive():
                logger.error((
                    'Error in main task {} quit unexpected'
                    ).format(TASKS[i][0].__name__))
                p.join()
                np = Process(target=task,
                             args=args)
                np.start()
                tasks[i] = (np, args)
            sleep(600)


if __name__ == '__main__':
    main()
