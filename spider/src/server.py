# -*- coding: utf-8 -*-


import logging
from concurrent import futures
from multiprocessing import Process, Queue

from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

import grpc

import spider_pb2
import spider_pb2_grpc

from task import crawl, submit_rss_feed


JOBS_QUEUE = Queue()


def crawling(*args):
    while True:
        spids = JOBS_QUEUE.get()
        p = Process(target=crawl, args=(spids,))
        p.start()
        p.join()


class SpiderRpcServicer(spider_pb2_grpc.SpiderRpcServicer):
    def SubmitRssFeed(self, request, context):
        feed = {
                'url': request.url,
                'category': request.category,
                'item_content_xpath': request.item_content_xpath,
                'removed_xpath_nodes': request.removed_xpath_nodes[:],
                'css': request.css
        }
        try:
            submit_rss_feed(feed)
        except Exception as e:
            return spider_pb2.SubmitResult(
                    error=True,
                    message=str(e)
            )
        return spider_pb2.SubmitResult(error=False)

    def CrawlArticles(self, request, context):
        spids = request.spider[:]
        JOBS_QUEUE.put(spids)
        return spider_pb2.CrawlTaskResult(isrunning=True)


def serve(grpc_uri):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    spider_pb2_grpc.add_SpiderRpcServicer_to_server(
            SpiderRpcServicer(),
            server
    )
    server.add_insecure_port(grpc_uri)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    settings = get_project_settings()
    configure_logging(
        settings,
        install_root_handler=True
    )
    logger = logging.getLogger(__name__)
    p = Process(target=crawling, args=())
    logger.info('start crawl task')
    p.start()
    grpc_uri = settings['GRPC_URI']
    logger.info('grpc server start listening')
    serve(grpc_uri)
    p.terminate()
    logger.info('grpc server terminated')
