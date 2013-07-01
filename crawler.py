#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" simple async crawler """

import os
import gevent
import urllib2
import time
from gevent import monkey
from bs4 import BeautifulSoup
monkey.patch_all()

urls = ['http://www.sabado.pt', 'http://www.sapo.pt', 'http://www.visao.pt',
        'http://www.sign.io', 'http://www.ddns.pt', 'http://news.google.pt', 'http://www.dn.pt']


def makeSoup(url):
    print ('Starting %s' % url)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; FreeBSD amd64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11')]
    page = opener.open(url).read()
    soup = BeautifulSoup(page)
    html = soup.find('html')
    # imgs = [x['src'] for x in soup.findAll('img')]

    """ prepare the dir to store all the data """
    dir_name = 'pages/' + ''.join(url.split('//')[1:])
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    """ write extracted html """
    f = open(dir_name + '/html.txt', 'w')
    data = html.prettify().encode('UTF-8')
    f.write(data)
    f.close()
    print ('%s: %s bytes' % (url, len(page)))

startTime = time.time()
jobs = [gevent.spawn(makeSoup, url) for url in urls]
gevent.joinall(jobs)
print "Total time: %s" % (time.time() - startTime)
