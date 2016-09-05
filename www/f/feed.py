# -*- coding: utf-8 -*-


from flask import Blueprint, render_template


feed_page = Blueprint('feed_page',
                      __name__,
                      template_folder='template')


@feed_page.route('/rss', methods=['GET'])
def submit_atom():
    return render_template('rss.html')


@feed_page.route('/blog', methods=['GET'])
def submit_blog():
    return render_template('blog.html')
