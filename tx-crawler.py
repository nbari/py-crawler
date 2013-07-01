from twisted.web.client import getPage
from twisted.internet import reactor
import time

def errorHandler(error):
    print "An error has occurred: <%s>" % str(error)
    reactor.stop()

def crawl(output, url, starttime):
    print url, 'finished in', time.time() - starttime

def main(url):
    starttime = time.time()
    print 'fetching', url
    d = getPage(url)
    d.addCallback(crawl, url, starttime)
    d.addErrback(errorHandler)

if __name__ == '__main__':
    urls = ['http://www.sabado.pt','http://www.sapo.pt','http://www.visao.pt','http://www.sign.io','http://www.ddns.pt','http://news.google.pt','http://www.dn.pt']
    for url in urls:
        main(url)
    reactor.run()
