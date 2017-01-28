# -*- coding: utf-8 -*-


import logging
import sys
from time import sleep
import json
from functools import partial
import threading
from multiprocessing import Process

import pika

from scrapy.utils.project import get_project_settings

from task import crawl, gen_lxmlspider, gen_blogspider


settings = get_project_settings()


def consume(callback, jobs, ch, method, properties, body):
    logger = logging.getLogger(__name__)
    args = json.loads(body)
    p = Process(target=callback,
                args=(args,))
    logger.info('{} job starting ...'.format(callback.__name__))
    p.daemon = True
    p.start()
    jobs.append(p)


def task(callback, key):
    jobs = []
    url = '{}?heartbeat=3600'.format(settings['BROKER_URL'])
    connection = pika.BlockingConnection(pika.connection.URLParameters(url))
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_logs',
                             type='direct')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=key)

    def _process_data_events(connection, channel, queue_name, callback):
        callback_ = partial(consume, callback, jobs)
        channel.basic_consume(callback_,
                              queue=queue_name,
                              no_ack=True)
        while True:
            connection.process_data_events()
            for j in jobs:
                if not j.is_alive():
                    j.join()
            sleep(120)
    t = threading.Thread(target=_process_data_events,
                         args=(connection,
                               channel,
                               queue_name,
                               callback))
    t.setDaemon(True)
    t.start()


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
    consumers = [(Process(target=task,
                          args=_),
                  _) for _ in TASKS]
    sleep(60)
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
            sleep(120)


if __name__ == '__main__':
    main()
