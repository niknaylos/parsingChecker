from funcs import *

url = input('input url: ')
sitemapLinks = extractSitemapLinks(url)
sitemapUrl = ''
newsTagFlag = False
isArticle = False
if checkIfValidRobots(url):
    sitemapLinks = extractSitemapLinks(url)

    for i, sitemapUrl in enumerate(sitemapLinks):
        newsTagFlag = newsTagExists(sitemapUrl)
        publicationDate = publicationDateExists(sitemapUrl)[0]
        validDate = checkIfDateValid(publicationDate)

        if publicationDate and (validDate or validDate is None):
            locTag = processSitemap(sitemapUrl)
            if locTag:
                print(
                    f'Valid publication date {publicationDate} and loc tag found for sitemap {i + 1}, url: {sitemapUrl}')
                print(f'Loc Tag: {locTag}')
                print(f'News Tag Present: {newsTagFlag}')
                break  # Exit the loop if a valid locTag is found
        # else:
        #     print(f'Publication date in sitemap {i + 1} is too old, not valid or missing.')
    if checkType(locTag):
        print(f'{locTag} is an article')
        isArticle = True
    else:
        print(f'{locTag} is not an article')
        if newsTagFlag:
            isArticle = True
    if isArticle:
        lang = newsLangExists(sitemapUrl) or newsArticleLang(locTag)
        if not lang:
            print(f'No language attribute found')
        else:
            print(f'Language found')

else:
    print('Not valid due to missing or invalid robots.txt')

if not isArticle and newsTagFlag:
    print('Media is invalid')
else:
    print('Media is valid')
