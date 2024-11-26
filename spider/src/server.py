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
from task import submit_rss_feed, crawl_articles


logging.getLogger(__name__).addHandler(logging.NullHandler())
processes = deque()


class SpiderRpcServicer(spider_pb2_grpc.SpiderRpcServicer):
    def SubmitRssFeed(self, request, context):
        feed = {
                'url': request.url,
                'category': request.category,
                'item_content_xpath': request.item_content_xpath,
                'removed_xpath_nodes': request.removed_xpath_nodes[:]
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
        p = Process(target=crawl_articles, args=(spids,))
        p.daemon = True
        processes.append(p)
        return spider_pb2.CrawlTaskResult(isrunning=True)


def serve(settings):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    spider_pb2_grpc.add_SpiderRpcServicer_to_server(
            SpiderRpcServicer(),
            server
    )
    server.add_insecure_port(settings['GRPC_URI'])
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
    settings = get_project_settings()
    serve(settings)
