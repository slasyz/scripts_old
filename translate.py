#!/usr/bin/python
# coding: utf-8

import sys, json, re
from urllib import quote
from urllib2 import urlopen, HTTPError, Request

class WrongLanguage(Exception): pass

if len(sys.argv) < 3:
    print(u'Not enough parameters.\n./translate.py ORIGIN_LANG DEST_LANG TEXT')
    exit()

def main():
    LANG1, LANG2 = sys.argv[1:3]
    TEXT = ' '.join(sys.argv[3:])
    if (len(LANG1) != 2) or (len(LANG2) != 2):
        raise WrongLanguage()

    #res = json.loads(urlopen('http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&q=%s&langpair=%s%%7C%s' % (quote(TEXT), LANG1, LANG2)).read())
    url = 'http://translate.google.com/translate_a/t?text=%s&sl=%s&tl=%s&client=t&hl=en&multires=0' % (quote(TEXT), LANG1, LANG2)
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urlopen(request).read()
    res = re.sub(r',{2,}', ',', res).replace(',]', ']')  
    res = json.loads(res)
    print(res[0][0][0])
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(u'Exit by Ctrl+C.')
    #except IndexError:
    #    print(u'Translate is impossible.')
    except WrongLanguage:
        print(u'Wrong language.')
    except HTTPError:
        print(u'HTTP Error!')

