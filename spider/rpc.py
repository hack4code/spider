import logging
import sys
import time
import json
from multiprocessing import Process

import pika

from scrapy.utils.project import get_project_settings

from task import crawl, gen_lxmlspider, gen_blogspider


settings = get_project_settings()


def run(ch, method, properties, body):
    args = json.loads(body)['spiders']
    p = Process(target=crawl,
                args=(args,))
    p.start()
    p.join()


def lxmlspider(ch, method, properties, body):
    args = json.loads(body)
    gen_lxmlspider(args)


def blogspider(ch, method, properties, body):
    args = json.loads(body)
    gen_blogspider(args)


def task(callback, queue):
    host = settings['BROKER_URL']
    connection = pika.BlockingConnection(pika.connection.URLParameters(host))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(callback,
                          queue=queue,
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
    TASKS = [(run, settings['CRAWL_QUEUE_NAME']),
             (lxmlspider, settings['LXMLSPIDER_QUEUE_NAME']),
             (blogspider, settings['BLOGSPIDER_QUEUE_NAME'])]
    consumers = [(Process(target=task, args=_), _) for _ in TASKS]
    time.sleep(60)
    for p, _ in consumers:
        p.start()

    logger.info('rpc task running ...')
    for i, (p, args) in enumerate(consumers):
        logger.info('check task state ...')
        if not p.is_alive():
            consumers[i] = Process(target=task,
                                   args=args)
        time.sleep(120)


if __name__ == '__main__':
    main()
