# -*- coding: utf-8 -*-


import logging
import base64
from io import BytesIO
from urllib.parse import urljoin

from lxml.html import fromstring, HTMLParser
from PIL import Image as ImageLib

from scrapy.http import Request
from scrapy.pipelines.media import MediaPipeline

from ..exceptions import ImgException


logger = logging.getLogger(__name__)


class Image():
    IMAGE_MAX_WIDTH = 800

    def __init__(self, data):
        self._image = ImageLib.open(BytesIO(data))

    @property
    def size(self):
        return self._image.size

    @property
    def type(self):
        return self._image.format

    def optimize(self, q=75):
        image = self._image
        w, h = self._image.size
        if w > self.IMAGE_MAX_WIDTH:
            h = int(float(h)/w*self.IMAGE_MAX_WIDTH)
            w = self.IMAGE_MAX_WIDTH
            image = self._image.resize((w, h),
                                       ImageLib.ANTIALIAS)
        buf = BytesIO()
        image.save(buf,
                   format=self._image.format,
                   quality=q)
        return buf.getvalue()


class ImagesDlownloadPipeline(MediaPipeline):
    MEDIA_NAME = 'image'
    IMAGE_MAX_SIZE = 1024*256

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def get_media_requests(self, item, info):
        doc = item['content']
        if isinstance(doc,
                      (str, bytes)):
            doc = fromstring(doc,
                             parser=HTMLParser(encoding=item['encoding']))
            item['content'] = doc

        try:
            attr = self.spiderinfo.spider.image_url_attr
        except AttributeError:
            attr = 'src'

        urls = []
        for e in doc.xpath('//img'):
            if attr in e.attrib:
                url = e.get(attr).strip(' \t\n')
                if url.startswith('/'):
                    url = urljoin(item['link'].strip(),
                                  url)
                    if url.startswith('//'):
                        url = 'http:' + url
                urls.append((url, e))

        reqs = []
        for url, e in urls:
            if not url.startswith('data'):
                try:
                    r = Request(url,
                                meta={'img': e})
                except ValueError:
                    logger.error((
                        'Error in pipeline image create Request[{}]'
                        ).format(url))
                else:
                    reqs.append(r)
        return reqs

    def media_failed(self, failure, request, info):
        logger.error((
            'Error in spider {} pipeline image download[{}]'
            ).format(self.spiderinfo.spider.name,
                     request.url))
        try:
            attr = self.spiderinfo.spider.image_url_attr
            img = request.meta['img']
            src = img.get(attr)
            img.set('src',
                    src)
        except AttributeError:
            pass

    def media_downloaded(self, response, request, info):
        if response.status != 200:
            raise ImgException(
                'image status is {}'.format(response.status))
        if not response.body:
            raise ImgException('image size is 0')
        img = response.meta['img']
        src = response.url
        data = response.body
        imglen = len(data)
        img.set('src', src)
        try:
            image = Image(data)
            w, _ = image.size
            if imglen > self.IMAGE_MAX_SIZE:
                data = image.optimize()
            imgtype = image.type
        except OSError:
            logger.error((
                'Error in spider {} pipeline image Pillow '
                'image type not support[{}]'
                ).format(self.spiderinfo.spider.name,
                         src))
            try:
                imgtype = response.headers['Content-Type'].split('/')[-1]
            except KeyError:
                logger.error((
                    'Error in spider {} pipeline image Content-Type[{}]'
                    'not found'
                    ).format(self.spiderinfo.spider.name,
                             src))
                return
        img.set('source', src)
        data = base64.b64encode(data).decode('ascii')
        img.set('src',
                'data:image/{};base64,{}'.format(imgtype,
                                                 data))

    def item_completed(self, results, item, info):
        return item
