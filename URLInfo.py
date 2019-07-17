class URLInfo:
    def __init__(self, url):
        self._url = url
        self.secured = self._isSecured()
        self.domain, self.path = self._extractComp()
        self.uri = self.getAbsoluteURI()
    
    def _isSecured(self):
        if (self._url.startswith("https://")):
            return True
        return False

    def _extractComp(self):
        domain = self._url
        loc = "/"
        if (self._url.startswith("https://")):
            domain = domain[8:]
        elif (self._url.startswith("http://")):
            domain = domain[7:]
        try:
            pos = domain.index("/")
            dom = domain[0:pos]
            loc = domain[pos:]
        except:
            dom = domain
            loc = "/"
        return dom, loc

    def getAbsoluteURI(self):
        if (self.secured):
            return "https://" + self.domain + self.path
        else:
            return "http://" + self.domain + self.path
    
    def setPath(self, path):
        self.path = path
        
if __name__ == "__main__":
    pass