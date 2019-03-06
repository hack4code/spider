# -*- coding: utf-8 -*-


def extract_head(response):
    head = []
    for node in response.xpath('//script'):
        try:
            src = node.attrib['src']
        except KeyError:
            pass
        else:
            if 'MathJax' in src:
                head.append(node.get())
                continue
        text = node.xpath('.//text()').get()
        if text and 'MathJax' in text:
            head.append(node.get())
    return head
