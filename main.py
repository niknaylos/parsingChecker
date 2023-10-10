import requests
import re
from bs4 import BeautifulSoup


def checkIfExisting(url):
    """Check if url exists"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f'The URL {url} is valid and opens properly.')
            return True
        else:
            print(f'The URL {url} is not accessible. Status code: {response.status_code}')
            return False
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False


def checkIfValidRobots(url):
    """Check if robots.txt is present for url and sitemaps are present on robots.txt"""
    if checkIfExisting(url):
        try:
            response = requests.get(url + '/robots.txt', timeout=10)
            if response.status_code == 200:
                print('robots.txt exists')
                if 'Sitemap:' in response.text:
                    print('Sitemap found in robots.txt')
                    return True
                else:
                    print('No Sitemap found in robots.txt')
                    return checkSitemapXml(url)
            else:
                print('No robots.txt found. Checking for sitemap.xml')
                return checkSitemapXml(url)

        except requests.exceptions.RequestException as e:
            print(f'An error occurred: {e}')
            return False


def extractSitemapLinks(url):
    try:
        response = requests.get(url + '/robots.txt', timeout=10)
        if response.status_code == 200:
            sitemapLinks = re.findall(r'Sitemap:\s*(https?://\S+)', response.text, re.IGNORECASE)
            return sitemapLinks
        else:
            print(f'Failed to retrieve robots.txt from {url}/robots.txt. Status code: {response.status_code}')
            return None
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return None


def checkSitemapXml(url):
    """Check if /sitemap.xml is present"""
    try:
        response = requests.get(url + '/sitemap.xml', timeout=10)
        if response.status_code == 200:
            print(f'sitemap.xml is present at url: {url + "/sitemap.xml"}')
            return True
        else:
            print(f'No sitemap.xml found at url: {url + "/sitemap.xml"}. Status code: {response.status_code}')
            return False
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False

    """Parse sitemaps, check if <news:news> is present on sitemap,
   else flag it as False,
   put <loc> into variable,
   if no <loc> check if <sitemap> is present,
    try opening <sitemap>
    if no <sitemap> – invalid media
   repeat func
   if <loc> is present check if <lastmod> or <news:publication_date> is present
   check if publication date is not older than 2 months ago.
   check if <news:language> is present. If not – flag = False
   """

    """Check if metatags are present on webpage:
    a) og:type content: article
    b) og:locale OR html/lang OR Content-Type = "en"
    /// if both are not present – check if <news:language> flag is True, if not – media invalid
    """


def newsTagExists(sitemapUrl):
    try:
        response = requests.get(sitemapUrl, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            news_tags = soup.find_all('news:news')
            if news_tags:
                print(f'Tag <news:news> found in sitemap at {sitemapUrl}')
                return True
            else:
                print(f'Tag <news:news> not found in sitemap at {sitemapUrl}')
                return False
        else:
            print(f'Failed to retrieve sitemap from {sitemapUrl}. Status code: {response.status_code}')
            return False
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False


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

