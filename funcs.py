import requests
import re
from bs4 import BeautifulSoup as bs

def makeRequest(url, timeout=10):
    """Make an HTTP GET request and return the response object if successful."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False
def checkIfExisting(url):
    """Check if url exists"""
    try:
        response = makeRequest(url)
        if response:
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
            response = makeRequest(url + '/robots.txt')
            if response:
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
        response = makeRequest(url + '/robots.txt')
        if response:
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
        response = makeRequest(url + '/sitemap.xml')
        if response:
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
        response = makeRequest(sitemapUrl)
        if response:
            soup = bs(response.content, 'xml')
            news_tags = soup.find_all('news:news')
            if news_tags:
                # print(f'Tag <news:news> found in sitemap at {sitemapUrl}')
                return True
            else:
                # print(f'Tag <news:news> not found in sitemap at {sitemapUrl}')
                return False
        else:
            print(f'Failed to retrieve sitemap from {sitemapUrl}. Status code: {response.status_code}')
            return False
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False
def publicationDateExists(sitemapUrl):
    try:
        response = makeRequest(sitemapUrl)
        if response:
            soup = bs(response.content, 'xml')
            lastMod = soup.find_all('lastmod')
            pubdate = soup.find_all('news:publication_date')
            if lastMod:
                # print(f'lastmod is present for sitemap {sitemapUrl}')
                return True
            else:
                if pubdate:
                    # print(f'publication date is present for sitemap {sitemapUrl}')
                    return True
                else:
                    return False
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False
def retrieveLocation(sitemapUrl):
    try:
        response = makeRequest(sitemapUrl)
        if response:
            soup = bs(response.content, 'xml')
            location = soup.find_all('loc')
            if location:
                locationUrl = location[0].text
                try:
                    locationResponse = requests.get(locationUrl, timeout=10)
                    if locationResponse.status_code == 200:
                        return locationUrl
                    else:
                        return False
                except requests.exceptions.RequestException as e:
                    print(f'An error occurred: {e}')
                    return False
            else:
                print('no loc found')
                return False
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False