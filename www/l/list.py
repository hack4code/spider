# -*- coding: utf-8 -*-


from flask import Blueprint, render_template


list_page = Blueprint('list_page',
                      __name__,
                      template_folder='template')


@list_page.route('/p', methods=['GET'])
def list_spiders():
    return render_template('spiders.html')
