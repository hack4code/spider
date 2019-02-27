# -*- coding: utf-8 -*-


import base64
import logging
from io import BytesIO
from urllib.parse import urlparse, urljoin

from PIL import Image as ImageLib
from lxml.html import HtmlElement

from scrapy.http import Request
from scrapy.pipelines.media import MediaPipeline

from mydm.util import is_url


logger = logging.getLogger(__name__)


class Image:

    MAX_WIDTH = 1024

    def __init__(self, data):
        self._image = ImageLib.open(BytesIO(data))

    @property
    def size(self):
        return self._image.size

    @property
    def type(self):
        return self._image.format

    def optimize(self, quality=75):
        image = self._image
        width, height = image.size
        if width > self.MAX_WIDTH:
            height = int(float(height)/width*self.MAX_WIDTH)
            width = self.MAX_WIDTH
            image = image.resize(
                    (width, height),
                    ImageLib.ANTIALIAS
            )
        buffer = BytesIO()
        image.save(
                buffer,
                format=self.type,
                quality=quality,
        )
        return buffer.getvalue()


class ImagesDlownloadPipeline(MediaPipeline):

    MEDIA_NAME = 'image'
    MAX_SIZE = 1024*256

    def __init__(self, settings):
        super().__init__(settings=settings)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        pipe = cls(settings)
        pipe.crawler = crawler
        return pipe

    @property
    def spider(self):
        return self.spiderinfo.spider

    @property
    def spider_name(self):
        return self.spiderinfo.spider.name

    def need_optimize(self, size):
        if size < self.MAX_SIZE:
            return False
        return True

    def get_media_requests(self, item, info):
        doc = item['content']
        assert isinstance(doc, HtmlElement)
        attrs = {'src'}
        imgattr = getattr(
                self.spider,
                'image_url_attr',
                None,
        )
        if isinstance(imgattr, (list, tuple)):
            attrs = attrs.union(imgattr)
        elif imgattr:
            attrs.add(imgattr)

        urls = []
        for e in doc.xpath('//img'):
            for attr in attrs:
                if attr not in e.attrib:
                    continue
                url = e.get(attr).strip('\t\n\r ')
                if url.startswith('//'):
                    r = urlparse(item['link'])
                    url = r.scheme + url
                elif url.startswith('/'):
                    url = urljoin(item['link'], url)
                if not is_url(url):
                    continue
                else:
                    urls.append((url, e))
                    break
            else:
                logger.error(
                        "spider[%s] can't find link attribute of image",
                        self.spider_name
                )

        requests = []
        for url, e in urls:
            if url.startswith('data'):
                continue
            try:
                r = Request(url, meta={'img': e})
            except ValueError:
                logger.error('invalid url[%s]', url)
            else:
                requests.append(r)
        return requests

    def media_failed(self, failure, request, info):
        logger.error(
                'spider[%s] download image[%s] failed',
                self.spider_name,
                request.url
        )
        request.meta['img'].set('src', request.url)

    def media_downloaded(self, response, request, info):
        if not response.body:
            logger.error(
                    'spider[%s] got size 0 image[%s]',
                    self.spider_name
            )
            return
        img = response.meta['img']
        src = response.url
        data = response.body
        imgsize = len(data)
        try:
            image = Image(data)
            if self.need_optimize(imgsize):
                data = image.optimize()
            imgtype = image.type
        except OSError:
            logger.error(
                    'spider[%s] PIL open image[%s] failed',
                    self.spider_name,
                    src
            )
            try:
                imgtype = response.headers['Content-Type'].split('/')[-1]
            except KeyError:
                imgtype = src.split('.')[-1]
        img.set('source', src)
        data = base64.b64encode(data).decode('ascii')
        img.set('src', f'data:image/{imgtype.upper()};base64,{data}')

    def item_completed(self, results, item, info):
        return item
