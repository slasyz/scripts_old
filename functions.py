# coding: utf-8

# === paRSSer ===
# Разработчик: slasyz ( http://juick.com/sl , http://slasyz.blogspot.com/ )
# Лицензия: GNU GPL v3 ( http://www.gnu.org/licenses/gpl.html )

import os, re, urllib2, pycurl
from xml.dom.minidom import parseString
from datetime import datetime

from urllib import urlencode, unquote_plus
from StringIO import StringIO

API_KEY = 'e44f024998b4ccf7215bbc4242a2d00a'

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return rc

def notify(title, text):
    link_regexp = re.compile(r'(http://[A-Za-z0-9_/\.]*)')
    text = re.sub(link_regexp, r'<a href="\1">\1</a>', text)
    os.popen("notify-send -t 10000 -i '/usr/share/icons/Tango/32x32/actions/go-top.png' '%s' '%s'" % (title, text))

def upload(url, params = {}, cookies = '', headers = []): # 1 - headers; 2 - body
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
        text = StringIO()
        curl.setopt(pycurl.WRITEFUNCTION, text.write)
        curl.perform()
        
        code = curl.getinfo(pycurl.HTTP_CODE)
        if code == 304: # Если принят результат "Not Modified"
            return '304'
        else:
            return text.getvalue()

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
