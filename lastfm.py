#!/usr/bin/python
# coding: utf-8

#http://ws.audioscrobbler.com/2.0/\?method\=group.getMembers\&api_key\=e44f024998b4ccf7215bbc4242a2d00a\&group\=Juick.com

from functions import *
import sys

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
