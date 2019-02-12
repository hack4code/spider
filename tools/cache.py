#! /usr/bin/env python


from datetime import date

import requests


params = {
        'day': str(date.today())
}

r = requests.get('http://127.0.0.1/api/day', params=params).json()
try:
    data = r['data']
except KeyError:
    raise SystemExit(0)

for _, articles in data.items():
    for artile in articles:
        aid = artile[0]
        r = requests.get(f'http://127.0.0.1/a/{aid}')
        print(f'{aid}: {r.status_code}')
