# -*- coding: utf-8 -*-


from flask import Flask, request, jsonify

from task import crawl, gen_lxmlspider, gen_blogspider

# DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/crawl", methods=["POST"])
def run_spider():
    spiders = [sp for sp in request.form["spiders"].split(",")]
    crawl.delay(spiders)
    return jsonify(err=0, msg='ok')


@app.route("/feed/atom", methods=["POST"])
def gen_atom_spider():
    args = {k: v for k, v in request.form.items()}
    if 'url' not in args or 'category' not in args:
        return jsonify(err=1, msg='url or category needed')
    if args['url'] == '':
        return jsonify(err=1, msg='url or category is empty')
    if args['category'] == '':
        args['category'] = u'技术'
    try:
        if gen_lxmlspider.delay(args):
            return jsonify(err=0, msg='ok')
        else:
            return jsonify(err=2, msg="task error")
    except:
        return jsonify(err=3, msg="celery error")


@app.route("/feed/blog", methods=["POST"])
def gen_blog_spider():
    args = {k: v for k, v in request.form.items()}
    if 'url' not in args or 'category' not in args:
        return jsonify(err=1, msg='url or category needed')
    if args['url'] == '' or args['category'] == '':
        return jsonify(err=1, msg='url or category is empty')
    try:
        if gen_blogspider.delay(args):
            return jsonify(err=0, msg='ok')
        else:
            return jsonify(err=2, msg="task error")
    except:
        return jsonify(err=3, msg="celery error")
