from funcs import *

url = input('input url: ')
sitemapLinks = extractSitemapLinks(url)
sitemapUrl = ''
newsTagFlag = False
if checkIfValidRobots(url):
    for i in sitemapLinks[:]:
        if len(sitemapLinks) > 0:
            sitemapUrl = sitemapLinks[0]
            if newsTagExists(sitemapUrl):
                newsTagFlag = True
            sitemapLinks.pop(0)
        else:
            break
elif checkSitemapXml(url):
    sitemapUrl = url + '/sitemap.xml'
    if newsTagExists(sitemapUrl):
        newsTagFlag = True
print(newsTagFlag)
