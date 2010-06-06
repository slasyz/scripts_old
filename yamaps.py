#!/usr/bin/python
# coding: utf-8

from functions import upload
from xml.dom.minidom import parseString
from urllib import quote
from urllib2 import HTTPError
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

if __name__ == '__main__':
    try:
        long, lat = get_coordinats(OBJECT)
        print(u'Объект "%s":\nДолгота: %s;\nШирота: %s.' % (OBJECT.decode('UTF-8'), long, lat))
    except IndexError:
        print(u'Объект "%s" не найден.' % OBJECT.decode('UTF-8'))
    except KeyboardInterrupt:
        print(u'Выход по Ctrl+C.')
    except HTTPError:
        print(u'Ошибка!')
