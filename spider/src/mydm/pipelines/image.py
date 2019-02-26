# -*- coding: utf-8 -*-


import base64
import logging
from io import BytesIO
from urllib.parse import urlparse, urljoin

from PIL import Image as ImageLib
from lxml.html import fromstring, HTMLParser

from scrapy.http import Request
from scrapy.pipelines.media import MediaPipeline

from mydm.exceptions import ImgException


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

    def need_optimize(self, size):
        if size < self.MAX_SIZE:
            return False
        return True

    def get_media_requests(self, item, info):
        doc = item['content']
        if isinstance(doc, (str, bytes)):
            doc = fromstring(
                    doc,
                    parser=HTMLParser(encoding=item['encoding'])
            )
            item['content'] = doc

        try:
            attr = self.spiderinfo.spider.image_url_attr
        except AttributeError:
            attr = 'src'

        urls = []
        for e in doc.xpath('//img'):
            if attr in e.attrib:
                url = e.get(attr).strip('\t\n\r ')
                if url.startswith('//'):
                    r = urlparse(item['link'])
                    url = r.scheme + url
                elif url.startswith('/'):
                    url = urljoin(item['link'], url)
                urls.append((url, e))

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
                'spider[%s] failed to download image[%s]',
                self.spiderinfo.spider.name,
                request.url
        )
        try:
            attr = self.spiderinfo.spider.image_url_attr
            img = request.meta['img']
            src = img.get(attr)
            img.set('src', src)
        except AttributeError:
            pass

    def media_downloaded(self, response, request, info):
        if not response.body:
            raise ImgException('image size is 0')
        img = response.meta['img']
        src = response.url
        data = response.body
        imgsize = len(data)
        img.set('src', src)
        try:
            image = Image(data)
            if self.need_optimize(imgsize):
                data = image.optimize()
            imgtype = image.type
        except OSError:
            logger.error(
                    'spider[%s] got unsupported image type[%s]',
                    self.spiderinfo.spider.name,
                    src
            )
            try:
                imgtype = response.headers['Content-Type'].split('/')[-1]
            except KeyError:
                imgtype = src.split('.')[-1].upper()
        img.set('source', src)
        data = base64.b64encode(data).decode('ascii')
        img.set('src', f'data:image/{imgtype.upper()};base64,{data}')

    def item_completed(self, results, item, info):
        return item
