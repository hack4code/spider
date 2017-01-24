import time
from multiprocessing import Process
import json

import pika

from scrapy.utils.project import get_project_settings

from .spider import crawl, gen_lxmlspider, gen_blogspider


settings = get_project_settings()


def run(ch, method, properties, body):
    args = json.load(body)['spiders']
    p = Process(target=crawl,
                args=(args,))
    p.start()
    p.join()


def lxmlspider(ch, method, properties, body):
    args = json.load(body)
    gen_lxmlspider(args)


def blogspider(ch, method, properties, body):
    args = json.load(body)
    gen_blogspider(args)


def create_task(queue, callback):
    host = settings['BROKER_URL']
    queue = settings[queue]
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()
    channel.queue_declare(queue)
    channel.basic_consume(callback,
                          queue=queue,
                          no_ack=True)
    channel.start_cosuming()


def main():
    TASKS = [(crawl, settings['CRAWL_QUEUE_NAME']),
             (lxmlspider, settings['LXMLSPIDER_QUEUE_NAME']),
             (blogspider, settings['BLOGSPIDER_QUEUE_NAME'])]
    consumers = [(Process(target=create_task,
                          args=_).start(), _) for _ in TASKS]
    for i, (p, args) in enumerate(consumers):
        if not p.is_alive():
            consumers[i] = Process(target=create_task,
                                   args=args)
        time.sleep(120)
