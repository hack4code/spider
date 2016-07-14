# -*- coding: utf-8 -*-


import logging
import base64

from lxml.html import fromstring, tostring, HTMLParser

import StringIO
from PIL import Image as ImageLib

from scrapy.http import Request
from scrapy.pipelines.media import MediaPipeline

logger = logging.getLogger(__name__)


class ImgException(Exception):
    pass


class Image():
    IMAGE_MAX_WIDTH = 800

    def __init__(self, data):
        self._image = ImageLib.open(StringIO.StringIO(data))

    @property
    def size(self):
        return self._image.size

    @property
    def type(self):
        return self._image.format

    def optimize(self, quality=75):
        image = self._image
        w, h = self._image.size
        if w > self.IMAGE_MAX_WIDTH:
            h = int(float(h)/w*self.IMAGE_MAX_WIDTH)
            w = self.IMAGE_MAX_WIDTH
            image = self._image.resize((w, h), ImageLib.ANTIALIAS)
        buf = StringIO.StringIO()
        image.save(buf, format=self._image.format)
        return buf.getvalue()


class ImagesDlownloadPipeline(MediaPipeline):
    MEDIA_NAME = 'image'
    DEFAULT_ITEM_CONTENT_FIELD = 'content'
    IMAGE_MAX_SIZE = 1024*128

    @classmethod
    def from_settings(cls, settings):
        cls.ITEM_CONTENT_FIELD = settings.get('ITEM_CONTENT_FIELD',
                                              cls.DEFAULT_ITEM_CONTENT_FIELD)
        return cls()

    def get_media_requests(self, item, info):
        try:
            doc = fromstring(item[self.ITEM_CONTENT_FIELD],
                             parser=HTMLParser(encoding=item['encoding']))
        except TypeError:
            return []
        try:
            attr = self.spiderinfo.spider.image_url_attr
        except AttributeError:
            attr = 'src'
        urls = [(e.get(attr).strip(), e)
                for e in doc.xpath('//img') if attr in e.attrib]
        item._doc = doc
        return [Request(url, meta={'img': e})
                for (url, e) in urls if not url.startswith('data')]

    def media_failed(self, failure, request, info):
        logger.error('spider {} image download failed : {}'.format(
            self.spiderinfo.spider.name, request.url))

    def media_downloaded(self, response, request, info):
        img = response.meta['img']
        src = request.url
        if response.status != 200:
            raise ImgException(
                'image status is {}'.format(response.status))
        if not response.body:
            raise ImgException('image size is 0')
        data = response.body
        imglen = len(data)
        try:
            image = Image(data)
            if imglen > self.IMAGE_MAX_SIZE:
                data = image.optimize()
            img.set('source', src)
            imgtype = image.type
            data = base64.b64encode(data)
            img.set('src',
                    'data:image/{};base64,{}'.format(imgtype, data))
            w, _ = image.size
            if w < 400:
                img.set('style', 'float: right')
        except:
            # logger.exception('spider {} PIL open image failed: {}'.format(
            #     self.spiderinfo.spider.name, src))
            try:
                ext = response.headers['Content-Type']
                data = base64.b64encode(data)
                img.set('src',
                        'data:{};base64,{}'.format(ext, data))
            except KeyError:
                logger.warning(
                    'spider {} not found Content-Type: {}'.format(
                        self.spiderinfo.spider.name, src))

    def item_completed(self, results, item, info):
        item[self.ITEM_CONTENT_FIELD] = tostring(item._doc, pretty_print=True)
        del item._doc
        return item
