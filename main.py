from funcs import *

url = input('input url: ')
sitemapLinks = extractSitemapLinks(url)
sitemapUrl = ''
newsTagFlag = False
if checkIfValidRobots(url):
    sitemapLinks = extractSitemapLinks(url)

    for i, sitemapUrl in enumerate(sitemapLinks):
        newsTagFlag = newsTagExists(sitemapUrl)
        publicationDate = publicationDateExists(sitemapUrl)[1]
        validDate = checkIfDateValid(publicationDate)

        if publicationDate and (validDate or validDate is None):
            locTag = processSitemap(sitemapUrl)
            if locTag:
                print(f'Valid publication date {publicationDate} and loc tag found for sitemap {i + 1}, url: {sitemapUrl}')
                print(f'Loc Tag: {locTag}')
                print(f'News Tag Present: {newsTagFlag}')
                break  # Exit the loop if a valid locTag is found
        # else:
        #     print(f'Publication date in sitemap {i + 1} is too old, not valid or missing.')
            """todo : only check if date could be incorrect and notify instead of stopping script"""
else:
    print('Not valid due to missing or invalid robots.txt')

