class PageInfo:
    def __init__(self, page_url):
        self.page_url = page_url
        self.links = list()
        self.images = list()
    
    def getPageLinks(self):
        return self.links
    
    def getImageLinks(self):
        return self.images
    
    def addPageLink(self, pageLink):
        self.links.append(pageLink)
    
    def addImageLink(self, imageLink):
        self.images.append(imageLink)

    def addPageLinks(self, pageLinks):
        pl = set(self.links)
        pl.update(pageLinks)
        self.links = list(pl)

    def addImageLinks(self, imageLinks):
        il = set(self.images)
        il.update(imageLinks)
        self.images = list(il)