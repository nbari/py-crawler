from twisted.web.client import getPage
from twisted.internet import reactor
import os
import time
from bs4 import BeautifulSoup


def errorHandler(error):
    print "An error has occurred: <%s>" % str(error)
    reactor.stop()


def makeSoup(page, url, starttime):
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
    print "url: %s bytes: %s finished in: %s" % (url, len(page), time.time() - starttime)


def crawl(url):
    starttime = time.time()
    print 'fetching', url
    d = getPage(url, agent='twisted example')
    d.addCallback(makeSoup, url, starttime)
    d.addErrback(errorHandler)

if __name__ == '__main__':
    urls = [
        'http://www.sabado.pt', 'http://www.sapo.pt', 'http://www.visao.pt',
        'http://www.sign.io', 'http://www.ddns.pt', 'http://news.google.pt', 'http://www.dn.pt']
    for url in urls:
        crawl(url)
    reactor.run()
