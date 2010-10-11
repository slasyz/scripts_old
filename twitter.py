#!/usr/bin/python
# coding: utf-8

import pycurl
from optparse import OptionParser
from urllib import urlencode
from urllib2 import HTTPError
from StringIO import StringIO

class TooLong(Exception): pass
class AuthError(Exception): pass

def upload(url, params = {}, auth = ''):
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, str(url))
    curl.setopt(pycurl.POST, 1)
    curl.setopt(pycurl.POSTFIELDS, urlencode(params))
    curl.setopt(pycurl.USERPWD, auth)
    text = StringIO()
    curl.setopt(pycurl.WRITEFUNCTION, text.write)
    curl.perform()
    
    code = curl.getinfo(pycurl.HTTP_CODE)
    return text.getvalue()

def main():
    parser = OptionParser()
    parser.add_option('-u', '--username',
                      type="str", dest="username", default = '',
                      help='Twitter account username.')
    parser.add_option('-p', '--password',
                      type="str", dest="password", default = '',
                      help='Twitter account password.')
    
    args, text = parser.parse_args()
    text = ' '.join(text)
    
    if not (args.username and args.password) or len(text) == 0:
        raise AuthError()
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
    except AuthError:
        print(u'Требуется имя пользователя, пароль и текст сообщения.')
    except HTTPError:
        print(u'Ошибка!')
