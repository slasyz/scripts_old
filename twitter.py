#!/usr/bin/python
# coding: utf-8

from functions import upload
from urllib2 import HTTPError
from optparse import OptionParser

class TooLong(Exception): pass

def main():
    parser = OptionParser()
    parser.add_option('-u', '--username',
                      type="str", dest="username",
                      help='Twitter account username.')
    parser.add_option('-p', '--password',
                      type="str", dest="password",
                      help='Twitter account password.')
    
    args, text = parser.parse_args()
    text = ' '.join(text)
    
    if len(text) > 140:
        raise TooLong()
    res = upload('http://twitter.com/statuses/update.xml', {'status': text}, auth = '%s:%s' % (args.username, args.password))
    print(u'Сообщение отправлено.')

if __name__ == '__main__':
    try:
        main()
    except TooLong:
        print(u'Сообщение слишком большое (максимальная длина - 140 символов)')
    except KeyboardInterrupt:
        print(u'Выход по Ctrl+C.')
    except HTTPError:
        print(u'Ошибка!')
