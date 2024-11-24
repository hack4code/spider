# -*- coding: utf-8 -*-


import base64
import logging
from io import BytesIO
from urllib.parse import urlparse, urljoin

from lxml.html import HtmlElement
from PIL import Image as ImageLib, ImageOps

from scrapy.http import Request
from scrapy.pipelines.media import MediaPipeline

from mydm.utils import is_url


logger = logging.getLogger(__name__)


class Image:

    MAX_WIDTH = 1024

    def __init__(self, data, type=None):
        self._image = ImageLib.open(BytesIO(data))

    @property
    def size(self):
        return self._image.size

    @property
    def type(self):
        return self._image.format

    def resize(self, quality=100):
        image = self._image
        width, height = image.size
        if width > self.MAX_WIDTH:
            ratio = float(height) / float(width)
            width = self.MAX_WIDTH
            height = int(width * ratio)
            image = ImageOps.fit(image, (width, height))
        buffer = BytesIO()
        image.save(
                buffer,
                format=self.type,
                quality=quality
        )
        return buffer.getvalue()


class ImagesDlownloadPipeline(MediaPipeline):
    MEDIA_NAME = 'image'
    MAX_SIZE = 1024*256

    def __init__(self, crawler):
        super().__init__(crawler=crawler)
        self._category_filter = crawler.settings['IMAGE_OPTIMIZE_CATEGORY_FILTER']
        self._invalid_img_element = []

    @classmethod
    def from_crawler(cls, crawler):
        pipe = cls(crawler)
        return pipe

    @property
    def spider(self):
        return self.spiderinfo.spider

    @property
    def spider_name(self):
        return self.spiderinfo.spider.name

    @property
    def spider_category(self):
        return self.spiderinfo.spider.category

    def need_resize(self, size):
        if size < self.MAX_SIZE:
            return False
        return True

    def get_media_requests(self, item, info):
        self._invalid_img_element = []
        doc = item['content']
        assert isinstance(doc, HtmlElement)
        attrs = {'src'}
        img_attr = getattr(
                self.spider,
                'image_url_attr',
                None,
        )
        if isinstance(img_attr, (list, tuple)):
            attrs = attrs.union(img_attr)
        elif img_attr:
            attrs.add(img_attr)

        urls = []
        for e in doc.xpath('//img'):
            def format_url(url, item):
                url = url.strip('\r\n\t ')
                if url.startswith('//'):
                    scheme = urlparse(item['link']).scheme
                    url = f'{scheme}:{url}'
                elif url.startswith('/'):
                    url = urljoin(item['link'], url)
                return url

            if 'srcset' in e.attrib:
                srcset = e.get('srcset')
                url = srcset.split(',')[0].split(' ')[0]
                url = format_url(url, item)
                if is_url(url):
                    urls.append((url, e))
                    e.attrib.pop('srcset')
                    continue
            for attr in attrs:
                if attr not in e.attrib:
                    continue
                url = e.get(attr)
                url = format_url(url, item)
                if not is_url(url):
                    continue
                else:
                    urls.append((url, e))
                    break
            else:
                logger.error(
                        "spider[%s] can't find image link attribute",
                        self.spider_name
                )
                self._invalid_img_element.append(e)
        requests = []
        for url, e in urls:
            if url.startswith('data'):
                continue
            try:
                request = Request(url, meta={'image_xpath_node': e})
            except ValueError:
                logger.error(
                        'spider[%s] got invalid url[%s]',
                        self.spider_name,
                        url
                )
            else:
                requests.append(request)
        return requests

    def media_failed(self, failure, request, info):
        logger.error(
                'spider[%s] download image[%s] failed:\n%s',
                self.spider_name,
                request.url,
                failure
        )

    def media_downloaded(self, response, request, info):
        if not response.body:
            logger.error(
                    'spider[%s] got size 0 image[%s]',
                    self.spider_name,
                    request.url
            )
            self._invalid_img_element.append(
                    response.meta['image_xpath_node']
            )
            return
        image_xpath_node = response.meta['image_xpath_node']
        src = response.url
        data = response.body
        image_size = len(data)
        try:
            image_type = response.headers['Content-Type'].split('/')[-1]
        except Exception:
            image_type = src.split('?')[0].split('.')[-1]
        image_type = image_type.upper()
        try:
            image = Image(data, type=image_type)
        except (OSError, IOError) as e:
            logger.error(
                    'spider[%s] PILLOW open image[%s, %s] failed[%s]',
                    self.spider_name,
                    src,
                    image_type,
                    e
            )
        else:
            if self.spider_category in self._category_filter:
                width, _ = image.size
                factor = 1
                while True:
                    new_width = width // factor
                    if new_width <= 800:
                        width = new_width
                        break
                    factor = factor + 1
                image_xpath_node.set('width', f'{width}px')
            elif self.need_resize(image_size):
                data = image.resize()
            image_type = image.type.upper()
        image_xpath_node.set('source', src)
        data = base64.b64encode(data).decode('ascii')
        if image_type == 'SVG':
            type = 'SVG+xml'
        else:
            type = image_type
        image_xpath_node.set(
                'src',
                f'data:image/{type};base64,{data}'
        )

    def item_completed(self, results, item, info):
        for e in self._invalid_img_element:
            e.drop_tree()
        self._invalid_img_element = []
        return item

    def file_path(self, request, response, info, *, item):
        raise NotImplementedError()

    def media_to_download(self, request, info, *, item):
        pass
