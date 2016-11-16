# -*- coding: utf-8 -*-


from datetime import datetime
from flask import Blueprint

from d import show_entries


home_page = Blueprint('home_page',
                      __name__,
                      template_folder='template')


@home_page.route('/', methods=['GET'])
def home():
    today = str(datetime.utcnow().date())
    return show_entries(today)
