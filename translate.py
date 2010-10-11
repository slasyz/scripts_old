#!/usr/bin/python
# coding: utf-8

import sys, json
from urllib import quote
from urllib2 import urlopen, HTTPError

if len(sys.argv) < 3:
    print(u'Недостаточно параметров.\n./translate.py ORIGIN_LANG DEST_LANG TEXT')
    exit()

def main():
    LANG1, LANG2 = sys.argv[1:3]
    TEXT = ' '.join(sys.argv[3:])
    if (len(LANG1) != 2) or (len(LANG2) != 2):
        raise WrongLanguage()

    res = json.loads(urlopen('http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&q=%s&langpair=%s%%7C%s' % (quote(TEXT), LANG1, LANG2)).read())
    print(res['responseData']['translatedText'])
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(u'Выход по Ctrl+C.')
    except IndexError:
        print(u'Перевод невозможен.')
    except TypeError:
        print(u'Неправильный язык.')
    except HTTPError:
        print(u'Ошибка!')

