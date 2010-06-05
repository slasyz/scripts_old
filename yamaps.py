#!/usr/bin/python
# coding: utf-8

from functions import upload
from urllib import quote
from xml.dom.minidom import parseString
import sys

if len(sys.argv) < 2:
    print(u'Недостаточно параметров.\n./yamaps.py OBJECT')
    exit()

API_KEY = 'AOcWCkwBAAAAHtxYBAQA-dHgCyJmgoQi5nla9n1EU5mzB6UAAAAAAAAAAADIkjLbzu5uacEGjlf6Lu2MrAb-UA=='
OBJECT = ' '.join(sys.argv[1:])

def get_coordinats(query):
    xml = upload(u'http://geocode-maps.yandex.ru/1.x/?geocode=%s&key=%s' % (quote(query), API_KEY))
    obj = parseString(xml)
    return obj.getElementsByTagName('pos')[0].childNodes[0].data.split(' ') # Долгота, широта

try:
    long, lat = get_coordinats(OBJECT)
    print(u'Объект "%s":\nДолгота: %s;\nШирота: %s.' % (OBJECT.decode('UTF-8'), long, lat))
except IndexError:
    print(u'Объект "%s" не найден.' % OBJECT.decode('UTF-8'))
