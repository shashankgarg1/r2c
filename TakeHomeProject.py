import http.client
from urllib.parse import urljoin
from queue import Queue
from bs4 import BeautifulSoup
import argparse
from URLInfo import URLInfo
from PageInfo import PageInfo
import json

domain = None
pages = None
result = None

def setDomain(urlInfo):
    global domain
    domain = urlInfo.domain

def getDomain():
    return domain

def resolveURL(urlInfo, url):
    return urljoin(urlInfo.getAbsoluteURI(), url)

def initializePages():
    global pages
    pages = Queue()

def addPages(urlInfo):
    pages.put(urlInfo)

def initializeResult():
    global result
    result = dict()

def resolveLinks(urlInfo, links):
    uris = set()
    while (not links.empty()):
        link = links.get()
        resolvedLink = resolveURL(urlInfo, link)
        uris.add(resolvedLink)
    return uris

def work():
    while (not pages.empty()):
        urlInfo = pages.get()
        absoluteURI = urlInfo.getAbsoluteURI()
        if (absoluteURI not in result and urlInfo.domain == getDomain()):
            result[absoluteURI] = PageInfo(absoluteURI)
            try:
                if (urlInfo.secured):
                    connection = http.client.HTTPSConnection(urlInfo.domain)
                else:
                    connection = http.client.HTTPConnection(urlInfo.domain)
                
                connection.request("GET", urlInfo.path)
                response = connection.getresponse()
                if (response.status == 200):
                    pageLinks = Queue()
                    imageLinks = Queue()
                    body = response.read().decode("utf-8")
                    soup = BeautifulSoup(body, "html.parser")
                    for pageLink in soup.find_all("a"):
                        pageLinks.put(pageLink.get("href"))
                    for imageLink in soup.find_all("img"):
                        imageLinks.put(imageLink.get("src"))

                    imageLinks = resolveLinks(urlInfo, imageLinks)
                    pageLinks = resolveLinks(urlInfo, pageLinks)
                    result[absoluteURI].addImageLinks(imageLinks)
                    result[absoluteURI].addPageLinks(pageLinks)
                    for pageLink in pageLinks:
                        newURLInfo = URLInfo(pageLink)
                        addPages(newURLInfo)

                elif (response.status >= 300 and response.status < 400):
                    location = response.getheader("Location")
                    uri = resolveURL(urlInfo, location)
                    addPages(URLInfo(uri))
            finally:
                connection.close()

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump([result[p].__dict__ for p in result], f, ensure_ascii=False, indent=4)
    
def main():
    print("starting")
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True, help="e.g. returntocorp.com")
    opt = parser.parse_args()

    urlInfo = URLInfo(opt.domain)
    setDomain(urlInfo)
    urlInfo.setPath("/")

    initializePages()
    initializeResult()

    addPages(urlInfo)
    work()

if __name__ == '__main__':
    main()