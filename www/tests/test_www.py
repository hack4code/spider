# -*- coding: utf-8 -*-


import random
from datetime import timedelta

import pytest

from flask import json

from app import app

from model import (
    get_after_day, get_end_day, get_begin_day,
    get_all_aids, get_spiders,
)


@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    return app.test_client()


class TestWWW:

    def test_home(self, client):
        rv = client.get('/')
        assert 200 == rv.status_code

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
            assert 200 == rv.status_code
            if day == end:
                break
            day = get_after_day(day)

    def test_api_spiders(self, client):
        rv = client.get('/api/spiders')
        data = json.loads(rv.data)
        assert 'entries' in data

    def test_api_categories(self, client):
        rv = client.get('/api/categories')
        data = json.loads(rv.data)
        assert 'data' in data

    def test_api_day(self, client):
        firstday = get_begin_day()
        rv = client.get(f'/api/day?day={firstday}')
        data = json.loads(rv.data)
        assert 'data' in data

        day = get_after_day(firstday)
        if day:
            rv = client.get(f'/api/day?day={day}')
            data = json.loads(rv.data)
            assert 'data' in data

        # invalid day
        rv = client.get('/api/day')
        assert 400 in rv.status_code
        rv = client.get('/api/day?day=2.3.2')
        assert 400 in rv.status_code
        noday = firstday - timedelta(days=1)
        rv = client.get(f'/api/day?day={noday}')
        assert 204 == rv.status_code
        data = json.loads(rv.data)
        assert 'message' in data

    def test_api_entries(self, client):
        spiders = get_spiders()
        spid = random.choice(spiders)

        rv = client.get(f'/api/entries?spid={spid}')
        data = json.loads(rv.data)
        if 200 == rv.status_code:
            assert 'entries' in data
        else:
            assert 400 == rv.status_code
            assert 'message' in data
