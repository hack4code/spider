# -*- coding: utf-8 -*-


import unittest
from app import app
from model import get_categories, get_articles, get_all_days, \
    get_before_day, get_after_day, get_all_articles, get_end_day, \
    get_begin_day


class WwwTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_home(self):
        print("test home page")
        rv = self.app.get('/home/')
        assert '<ul id="category">' in rv.data.decode('utf8')

    def test_all_aids(self):
        for aid in get_articles():
            rv = self.app.get('/a/{}'.format(aid))
            assert '<article' in rv.data.decode('utf8')

    def test_invalid_aid(self):
        rv = self.app.get('/a/-1')
        assert '<title>400</title>' in rv.data.decode('utf8')
        rv = self.app.get('/a/x1')
        assert '<title>400</title>' in rv.data.decode('utf8')
        rv = self.app.get('/a/x')
        assert '<title>400</title>' in rv.data.decode('utf8')

    def test_all_days(self):
        print("test page of all days")
        for day in get_all_days():
            day_end = get_end_day()
            day_begin = get_begin_day()
            if day == day_end or day == day_begin:
                continue
            print('day: {}'.format(day))
            day_before = get_before_day(day)
            day_after = get_after_day(day)
            rv = self.app.get('/d/{}'.format(day))
            print(str(day_before))
            print(str(day_after))
            assert '<ul id="category">' in rv.data.decode('utf8')
            assert '/d/{}'.format(day_after) in rv.data.decode('utf8')
            assert '/d/{}'.format(day_before) in rv.data.decode('utf8')

    def test_invalid_day(self):
        rv = self.app.get('/d/2015-04-02')
        assert '<title>404</title>' in rv.data.decode('utf8')
        rv = self.app.get('/d/20222')
        assert '<title>400</title>' in rv.data.decode('utf8')
        rv = self.app.get('/d/2222-01-01')
        assert '<title>404</title>' in rv.data.decode('utf8')
        rv = self.app.get('/d/1000-01-01')
        assert '<title>404</title>' in rv.data.decode('utf8')

    def test_invalid_category(self):
        rv = self.app.get('/c/1')
        assert '<title>400</title>' in rv.data.decode('utf8')

    def test_list_categories(self):
        rv = self.app.get('/l/c')
        assert '<ul id="clist">' in rv.data.decode('utf8')

    def test_categories(self):
        categories = get_categories()
        for c in categories:
            rv = self.app.get(u'/c/%s' % (c,))
            assert '<ul id="alist">' in rv.data.decode('utf8')
            articles = get_all_articles(c)
            for a in articles[2:]:
                print('category={} aid={} q=n'.format(c, a.id))
                rv = self.app.get(u'/c/{}?aid={}&q=n'.format(c, a.id))
                assert '<ul id="alist">' in rv.data.decode('utf8')
            for a in articles[:-2]:
                print('category={} aid={} q=p'.format(c, a.id))
                rv = self.app.get(u'/c/{}?aid={}&q=p'.format(c, a.id))
                assert '<ul id="alist">' in rv.data.decode('utf8')

    def test_cache(self):
        day = get_end_day()
        rv = self.app.get('/d/{}'.format(day))
        assert 'no-cache' == rv.headers['Cache-Control']
        rv = self.app.get('/home/')
        assert 'no-cache' == rv.headers['Cache-Control']
        day_before = get_before_day(day)
        rv = self.app.get('/d/{}'.format(day_before))
        assert int(rv.headers['Cache-Control'].split('=')[1]) > 60*60*12

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(WwwTestCase('test_cache'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
