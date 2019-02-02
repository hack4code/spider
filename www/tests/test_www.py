# -*- coding: utf-8 -*-


import random
import pytest

from app import app

from model import (
    get_categories,
    get_all_aids, get_aids_by_category,
    get_before_day, get_after_day, get_end_day, get_begin_day
)


@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    return app.test_client()


class TestWWW:

    def test_home(self, client):
        rv = client.get('/')
        assert '200 OK' == rv.status

    def test_aids(self, client):
        aids = get_all_aids()
        random.shuffle(aids)
        for aid in aids[:8]:
            rv = client.get('/a/{}'.format(aid))
            assert '<article' in rv.data.decode('utf8')

    def test_invalid_aid(self, client):
        rv = client.get('/a/-1')
        assert '<title>404</title>' in rv.data.decode('utf8')
        rv = client.get('/a/x1')
        assert '<title>404</title>' in rv.data.decode('utf8')
        rv = client.get('/a/x')
        assert '<title>404</title>' in rv.data.decode('utf8')

    def test_days(self, client):
        end = get_end_day()
        day = get_begin_day()
        for _ in range(3):
            rv = client.get(f'/d/{day}')
            assert '200 OK' == rv.status
            if day == end:
                break
            day = get_after_day(day)
