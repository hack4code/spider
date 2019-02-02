# -*- coding: utf-8 -*-


import random
import pytest

from model import (
    get_categories,
    get_all_aids, get_aids_by_category,
    get_before_day, get_after_day, get_end_day, get_begin_day
)


@pytest.fixture(scope='module')
def client():
    from app import app

    app.config['TESTING'] = True
    app.app_context().push()
    yield app.test_client()
    app.app_context.pop()


class TestWWW:

    def test_home(self, client):
        rv = client.get('/home/')
        assert '<ul id="category">' in rv.data.decode('utf8')

    def test_all_aids(self, client):
        aids = get_all_aids()
        random.shuffle(aids)
        for aid in aids[:8]:
            rv = client.get('/a/{}'.format(aid))
            assert '<article' in rv.data.decode('utf8')

    def test_invalid_aid(self, client):
        rv = client.get('/a/-1')
        assert '<title>400</title>' in rv.data.decode('utf8')
        rv = client.get('/a/x1')
        assert '<title>400</title>' in rv.data.decode('utf8')
        rv = client.get('/a/x')
        assert '<title>400</title>' in rv.data.decode('utf8')

    def test_days(self, client):
        end = get_end_day()
        day = get_begin_day()
        for _ in range(3):
            day_before = get_before_day(day)
            day_after = get_after_day(day)
            rv = client.get('/d/{}'.format(day))
            assert '<ul id="category">' in rv.data.decode('utf8')
            assert '/d/{}'.format(day_after) in rv.data.decode('utf8')
            assert '/d/{}'.format(day_before) in rv.data.decode('utf8')
            if day == end:
                break

    def test_invalid_day(self, client):
        rv = client.get('/d/2015-04-02')
        assert '<title>404</title>' in rv.data.decode('utf8')
        rv = client.get('/d/20222')
        assert '<title>400</title>' in rv.data.decode('utf8')
        rv = client.get('/d/2222-01-01')
        assert '<title>404</title>' in rv.data.decode('utf8')
        rv = client.get('/d/1000-01-01')
        assert '<title>404</title>' in rv.data.decode('utf8')

    def test_categories(self, client):
        categories = get_categories()
        for category in categories:
            rv = client.get(f'/c/{category}')
            assert '<ul id="alist">' in rv.data.decode('utf8')
            aids = get_aids_by_category(category)
            for aid in aids[2:][:8]:
                rv = client.get(f'/c/{category}?aid={aid.aid}&q=n')
                assert '<ul id="alist">' in rv.data.decode('utf8')
            for aid in aids[:-2][:8]:
                rv = client.get(f'/c/{category}?aid={aid.aid}&q=p')
                assert '<ul id="alist">' in rv.data.decode('utf8')
