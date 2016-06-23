# -*- coding: utf-8 -*-


from flask import Blueprint, render_template
from model import get_spiders


list_page = Blueprint('list_page',
                      __name__,
                      template_folder='template')


@list_page.route('/p', methods=['GET'])
def list_spiders():
    return render_template('spiders.html', spiders=get_spiders())
