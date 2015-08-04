#!/usr/bin/env python

# -*- coding: UTF-8 -*-

import re
import requests
import PyV8

class FrenchTorrentDB:
    
    urls = {
        'home':               'http://www.frenchtorrentdb.com/',
        'login':              'http://www.frenchtorrentdb.com/?section=LOGIN&ajax=1',
        'loginChallenge':     'http://www.frenchtorrentdb.com/?section=LOGIN&challenge=1',
        'loginCheck':         'http://www.frenchtorrentdb.com/',
        'search':             'http://www.frenchtorrentdb.com/',
        'download':           'http://www.frenchtorrentdb.com/'
    }

    def __init__(self, username, password):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31'})

        self.username = username
        self.password = password

    def login(self):

        # Get challenge
        r = self.session.get(self.urls['loginChallenge'])
        data = r.json()

        # Prepare data to send for login
        postData = {
            'username': self.username,
            'password': self.password,
            'hash': data['hash'],
            'secure_login' : ''
        }

        # Evaluate the challenge data to send back for login
        with PyV8.JSLocker():
            ctxt = PyV8.JSContext()
            ctxt.enter()

            ctxt.eval("var hash = '"+ data['hash'] +"';")
            ctxt.eval("var challenge = '';")
            ctxt.eval("var a = '05f';")
    
            for ch in data['challenge']:
                ctxt.eval("challenge += "+ ch +";")
    
            postData['secure_login'] = ctxt.eval("challenge;");
            ctxt.leave()
            
        # Login headers
        headers = {
            'Referer': 'http://www.frenchtorrentdb.com/?section=LOGIN',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }

        # Send login form
        r = self.session.post(self.urls['login'], data=postData, headers=headers)

        return self.checkLogin()


    def checkLogin(self):
    	# Fetch login check URL
        r = self.session.get(self.urls['loginCheck'])

    	return '<a href="/?section=LOGOUT">Logout</a>' in r.text


    def getRatio(self):
    	r = self.session.get(self.urls['home'])

    	return float(re.search('<div class="ratio"[^>]*>([^<]*)</div>', r.text).group(1))
