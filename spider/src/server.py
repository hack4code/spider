# -*- coding: utf-8 -*-


import sys
import time
import logging
from collections import deque
from concurrent import futures
from multiprocessing import Process

import grpc
from scrapy.utils.project import get_project_settings

import spider_pb2
import spider_pb2_grpc
from task import submit_rss_feed, submit_blog_feed, crawl_articles


processes = deque()


class SpiderRpcServicer(spider_pb2_grpc.SpiderRpcServicer):

    def SubmitRssFeed(self, request, context):
        feed = {
                'url': request.url,
                'category': request.category,
        }
        if len(request.removed_xpath_nodes) > 0:
            feed['removed_xpath_nodes'] = []
            for xpath in request.removed_xpath_nodes:
                feed['removed_xpath_nodes'].append(xpath)
        try:
            submit_rss_feed(feed)
        except Exception as e:
            return spider_pb2.SubmitResult(
                    error=True,
                    message=str(e)
            )
        return spider_pb2.SubmitResult(error=False)

    def SubmitBlogFeed(self, request, context):
        feed = {
                'url': request.url,
                'category': request.category,
                'entry_xpath': request.entry_xpath,
                'item_title_xpath': request.item_title_xpath,
                'item_link_xpath': request.item_link_xpath,
                'item_content_xpath': request.item_content_xpath
        }
        if len(request.removed_xpath_nodes) > 0:
            feed['removed_xpath_nodes'] = []
            for xpath in request.removed_xpath_nodes:
                feed['removed_xpath_nodes'].append(xpath)
        try:
            submit_blog_feed(feed)
        except Exception as e:
            return spider_pb2.SubmitResult(
                    error=True,
                    message=str(e)
            )
        return spider_pb2.SubmitResult(error=False)

    def CrawlArticles(self, request, context):
        spids = request.spider[:]
        p = Process(target=crawl_articles, args=(spids,))
        p.daemon = True
        processes.append(p)
        return spider_pb2.CrawlTaskResult(isrunning=True)


def init_logger():
    settings = get_project_settings()
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(settings['LOG_LEVEL'])
    handler.setFormatter(
            logging.Formatter(
                settings['LOG_FORMAT'],
                settings['LOG_DATEFORMAT']
            )
    )
    root.addHandler(handler)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    spider_pb2_grpc.add_SpiderRpcServicer_to_server(
            SpiderRpcServicer(),
            server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(60)
            if len(processes) == 0:
                continue
            p = processes[0]
            if p.is_alive():
                continue
            code = p.exitcode
            if code is None:
                p.start()
            else:
                p.join()
                processes.popleft()
                if len(processes) > 0:
                    processes[0].start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == '__main__':
    init_logger()
    logger = logging.getLogger(__name__)
    logger.info('grpc server running...')
    serve()
