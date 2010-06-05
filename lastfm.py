#!/usr/bin/python
# coding: utf-8

#http://ws.audioscrobbler.com/2.0/\?method\=group.getMembers\&api_key\=e44f024998b4ccf7215bbc4242a2d00a\&group\=Juick.com

from functions import *
from urllib2 import HTTPError
from xml.dom.minidom import parseString
from urllib import unquote_plus

import sys

API_KEY = 'e44f024998b4ccf7215bbc4242a2d00a' # Last.FM

def get_members(group):
    xml = upload('http://ws.audioscrobbler.com/2.0/?method=group.getMembers&api_key=%s&group=%s'%(API_KEY, group))
    obj = parseString(xml)
    num = int(obj.getElementsByTagName('members')[0].getAttribute('totalPages'))
    rc = []
    for page in xrange(num):
        xml = upload('http://ws.audioscrobbler.com/2.0/?method=group.getMembers&api_key=%s&group=%s&page=%s'%(API_KEY, group, page))
        obj = parseString(xml)
        for node in obj.getElementsByTagName('name'):
            rc.append(node.childNodes[0].data)
    return rc
    
def get_score(user1, user2):
    xml = upload('http://ws.audioscrobbler.com/2.0/?method=tasteometer.compare&api_key=%s&limit=0&type1=user&type2=user&value1=%s&value2=%s'%(API_KEY, user1, user2))
    return parseString(xml).getElementsByTagName('score')[0].childNodes[0].data

if len(sys.argv) < 4:
    print('Недостаточно параметров.\n./lastfm.py USER GROUP COUNT')
    exit()

def main():
    USER = sys.argv[1]
    GROUP = sys.argv[2]
    N = int(sys.argv[3])

    members = get_members(GROUP)
    scores = {}

    for m in members:
        scores[m] = get_score(USER, m)

    scores = list(scores.items())

    i = len(scores)
    while i > 1:
        for j in xrange(i - 1):
            if scores[j][1] < scores[j+1][1]:
                temp = scores[j]
                scores[j] = scores[j+1]
                scores[j+1] = temp
        i -= 1

    for i in xrange(1, N+1):
            print(u'%s: %i/100' % (scores[i][0], float(scores[i][1][:4])*100))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Выход по Ctrl+C.')
    except HTTPError:
        print('Группы или пользователя не существует.')
