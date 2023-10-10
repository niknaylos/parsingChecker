from funcs import *

url = input('input url: ')
sitemapLinks = extractSitemapLinks(url)
sitemapUrl = ''
newsTagFlag = False
lastmodFlag = False
if checkIfValidRobots(url):
    for i in sitemapLinks[:]:
        if newsTagFlag and lastmodFlag:
            break
        elif len(sitemapLinks) > 0:
            sitemapUrl = sitemapLinks[0]
            if publicationDateExists(sitemapUrl):
                lastmodFlag = True
                if newsTagExists(sitemapUrl):
                    newsTagFlag = True
                sitemapLinks.pop(0)
        else:
            break

if newsTagFlag and lastmodFlag:
    print(f'<news:news> and lastmod / publication date is available for at least one sitemap, url: {sitemapUrl}')
    loc = retrieveLocation(sitemapUrl)
    print(loc)
else:
    print('Not valid')

