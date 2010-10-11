#!/usr/bin/python -W ignore::DeprecationWarning
# coding: utf-8

import os, sys, xmpp
from optparse import OptionParser

def main():
    parser = OptionParser()
    parser.add_option('-j', '--jid', 
                      type="str", dest="jid", default='',
                      help='Bot\'s jid.')
    parser.add_option('-p', '--password', 
                      type="str", dest="password", default='',
                      help='Bot\'s password.')
    parser.add_option('-r', '--recipient', 
                      type="str", dest="recipient", default='',
                      help='Recipient\'s jid.')
                      
    args, text = parser.parse_args()
    text = ' '.join(text)

    jid = xmpp.JID(args.jid)
    password = args.password
    recipient = xmpp.JID(args.recipient)
    if text != '': message = text
    else: message = sys.stdin.read()

    res = xmpp.Client(jid.getDomain(), debug = 0)
    res.connect()
    res.auth(jid.getNode(), password, 'res')
    res.send(xmpp.Message(recipient, message, typ='chat'))
    res.disconnect()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(u'Выход по Ctrl+C.')
