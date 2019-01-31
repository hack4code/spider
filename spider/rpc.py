# -*- coding: utf-8 -*-


import logging
import sys
import json
from collections import deque
from time import sleep
from multiprocessing import Process

import pika

from scrapy.utils.project import get_project_settings

from task import crawl, gen_lxmlspider, gen_blogspider


SETTINGS = get_project_settings()


def task(callback, key):
    logger = logging.getLogger(__name__)
    consumers = deque()
    url = '{}?heartbeat=600'.format(SETTINGS['BROKER_URL'])
    connection = pika.BlockingConnection(pika.connection.URLParameters(url))
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(
            exchange='direct_logs',
            queue=queue_name,
            routing_key=key
    )
    channel.basic_qos(prefetch_count=1)

    def consume(ch, method, properties, body):
        logger.info('get job[%s] from rabbitmq', callback.__name__)
        args = json.loads(body)
        p = Process(target=callback, args=(args,))
        p.daemon = True
        consumers.append((p, ch, method))

    channel.basic_consume(consume, queue=queue_name)
    while True:
        connection.process_data_events()
        try:
            p, ch, method = consumers[0]
        except IndexError:
            pass
        else:
            if p.is_alive():
                continue
            status = p.exitcode
            if status is None:
                p.start()
            else:
                if status == 0:
                    logger.info('job[%s] finished', callback.__name__)
                else:
                    logger.error(
                            'job[%s] exited with %d',
                            callback.__name__,
                            status
                    )
                p.join()
                ch.basic_ack(delivery_tag=method.delivery_tag)
                consumers.popleft()


def main():
    def init_logger():
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(SETTINGS['LOG_LEVEL'])
        handler.setFormatter(
                logging.Formatter(
                    SETTINGS['LOG_FORMAT'],
                    SETTINGS['LOG_DATEFORMAT']
                )
        )
        root.addHandler(handler)

    init_logger()
    logger = logging.getLogger(__name__)
    TASKS = [
        (crawl, SETTINGS['CRAWL_KEY']),
        (gen_lxmlspider, SETTINGS['LXMLSPIDER_KEY']),
        (gen_blogspider, SETTINGS['BLOGSPIDER_KEY'])
    ]
    sleep(60)
    tasks = [(Process(target=task, args=_), _) for _ in TASKS]
    for p, _ in tasks:
        p.start()
    logger.info('rpc task running ...')
    while True:
        sleep(60)
        for i, (p, args) in enumerate(tasks):
            if p.is_alive():
                continue
            logger.error(
                'Error in main task %s quit unexpected',
                TASKS[i][0].__name__
            )
            p.join()
            np = Process(target=task, args=args)
            np.start()
            tasks[i] = (np, args)


if __name__ == '__main__':
    main()
