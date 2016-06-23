# -*- coding: utf-8 -*-


from flask import Blueprint, render_template

from model import get_categories


feed_page = Blueprint('feed_page',
                      __name__,
                      template_folder='template')


@feed_page.route('/atom', methods=['GET'])
def submit_atom():
    categories = get_categories()
    return render_template('atom.html', categories=categories)


@feed_page.route('/blog', methods=['GET'])
def submit_blog():
    categories = get_categories()
    return render_template('blog.html', categories=categories)
