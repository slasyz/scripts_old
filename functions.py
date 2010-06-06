# coding: utf-8

# === paRSSer ===
# Разработчик: slasyz ( http://juick.com/sl , http://slasyz.blogspot.com/ )
# Лицензия: GNU GPL v3 ( http://www.gnu.org/licenses/gpl.html )

import os, re, urllib2, pycurl
from datetime import datetime

from urllib import urlencode, unquote_plus
from StringIO import StringIO

def notify(title, text):
    link_regexp = re.compile(r'(http://[A-Za-z0-9_/\.]*)')
    text = re.sub(link_regexp, r'<a href="\1">\1</a>', text)
    os.popen("notify-send -t 10000 -i '/usr/share/icons/Tango/32x32/actions/go-top.png' '%s' '%s'" % (title, text))

def upload(url, params = {}, cookies = '', headers = [], auth = ''):
    if params == {}:
        return urllib2.urlopen(url).read()
    else:
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.POST, 1)
        data = []
        multipart = False
        for key, value in params.items():
            if value != '':
                if value[0] == '@':
                    data.append((key, (pycurl.FORM_FILE, value[1:])))
                    multipart = True
                else:
                    data.append((key, value))
            else:
                data.append((key, value))
        if multipart: # Если есть файлы, то отправляет multipart/form-data
            curl.setopt(pycurl.HTTPPOST, data)
        else:
            curl.setopt(pycurl.POSTFIELDS, urlencode(data))
        curl.setopt(pycurl.COOKIE, cookies)
        curl.setopt(pycurl.HTTPHEADER, headers)
        curl.setopt(pycurl.USERPWD, auth)
        text = StringIO()
        curl.setopt(pycurl.WRITEFUNCTION, text.write)
        curl.perform()
        
        code = curl.getinfo(pycurl.HTTP_CODE)
        if code == 304: # Если принят результат "Not Modified"
            return '304'
        else:
            return text.getvalue()
