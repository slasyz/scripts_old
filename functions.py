# coding: utf-8

# === SimpLoader ===
# Developed by: slasyz ( http://juick.com/sl )
# Home page: http://slasyz.github.com/simploader/
# License: GNU GPL v3 ( http://www.gnu.org/licenses/gpl.html )

import os, re, urllib2, pycurl, types, subprocess
from urllib import urlencode
from StringIO import StringIO

def upload(url, params = {}, cookies = '', headers = [], auth = '', part = 2): # 1 - headers, 2 - body
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, str(url))
    if params != {}:
        curl.setopt(pycurl.POST, 1)
        data = []
        multipart = False
        for key, value in params.items():
            if (value != '') and (type(value) == types.StringType):
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
    else:
        curl.setopt(pycurl.POST, 0)
    curl.setopt(pycurl.COOKIE, cookies)
    curl.setopt(pycurl.HTTPHEADER, headers)
    curl.setopt(pycurl.USERPWD, auth)
    text = StringIO()
    heads = StringIO()
    curl.setopt(pycurl.WRITEFUNCTION, text.write)
    curl.setopt(pycurl.HEADERFUNCTION, heads.write)
    curl.perform()
    
    code = curl.getinfo(pycurl.HTTP_CODE)
    if code == 304: # Если принят результат "Not Modified"
        return '304'
    else:
        return (heads.getvalue(), text.getvalue())[part-1]

def notify(title, text):
    link_regexp = re.compile(r'(http://[A-Za-z0-9_/\.]*)')
    text = re.sub(link_regexp, r'<a href="\1">\1</a>', text)
    return subprocess.call(['notify-send', '-t', '10000', '-i', 'go-top', title, text])
