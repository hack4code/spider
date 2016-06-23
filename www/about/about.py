# -*- coding: utf-8 -*-


from flask import render_template, Blueprint


about_page = Blueprint('about_page',
                       __name__,
                       template_folder='template')


# about page
@about_page.route('/', methods=['GET'])
def about():
    return render_template('about.html')
