#!/usr/bin/python
# coding: utf-8

import sys, json, urllib
from functions import upload

if len(sys.argv) < 3:
    print('Недостаточно параметров.\n./google.py COUNT TEXT')
    exit()
    
COUNT = int(sys.argv[1])
TEXT = ' '.join(sys.argv[2:])

results = []
for i in xrange(COUNT / 4 + 1):
    res = upload('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s&start=%i' % (urllib.quote(TEXT), i*4))
    json_res = json.loads(res)
    results += json_res['responseData']['results']

for i in xrange(COUNT):
    r = results[i]
    print('%i. \033[1;31m%s\033[0m\n%s\n\033[4;34m%s\033[0m\n' % (i+1, r['titleNoFormatting'], r['content'].replace('<b>', '').replace('</b>', ''), r['url']))
