import requests
import re
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import pytz


def makeRequest(url, timeout=10):
    """Make an HTTP GET request and return the response object if successful."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False


def checkIfValidRobots(url):
    """Check if robots.txt is present for url and sitemaps are present on robots.txt"""
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


def extractSitemapLinks(url):
    response = makeRequest(url + '/robots.txt')
    if response:
        sitemapLinks = re.findall(r'Sitemap:\s*(https?://\S+)', response.text, re.IGNORECASE)
        return sitemapLinks
    else:
        print(f'Failed to retrieve robots.txt from {url}/robots.txt. Status code: {response.status_code}')
        return False


def checkSitemapXml(url):
    """Check if /sitemap.xml is present"""
    response = makeRequest(url + '/sitemap.xml')
    if response:
        print(f'sitemap.xml is present at url: {url + "/sitemap.xml"}')
        return True
    else:
        print(f'No sitemap.xml found at url: {url + "/sitemap.xml"}. Status code: {response.status_code}')
        return False


def newsTagExists(sitemapUrl):
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


def publicationDateExists(sitemapUrl):
    response = makeRequest(sitemapUrl)
    if response:
        soup = bs(response.content, 'xml')
        lastMod = soup.find_all('lastmod')
        pubDate = soup.find_all('news:publication_date')
        realDate = []
        if lastMod:
            realDate = [tag.text for tag in lastMod]  # Extracting text content from the tags
            return realDate
        elif pubDate:
            realDate = [tag.text for tag in pubDate]  # Extracting text content from the tags
            return realDate
        else:
            return False


def processSitemap(sitemapUrl):
    response = makeRequest(sitemapUrl)
    if response:
        soup = bs(response.content, 'xml')
        locTags = soup.find_all('loc')
        sitemapTags = soup.find_all('sitemap')
        if len(sitemapTags) > 0:
            # Recursion to check for sitemap tags inside the sitemap if loc is not found
            for sitemapTag in sitemapTags:
                sitemapUrl = sitemapTag.find('loc').text
                nestedLocationUrl = processSitemap(sitemapUrl)
                if nestedLocationUrl:
                    return nestedLocationUrl  # Return the first working URL found during recursive calls
        for i, locTag in enumerate(locTags):
            if i >= 10:
                break
            locationUrl = locTag.text
            locationResponse = makeRequest(locationUrl)
            if locationResponse:
                return locationUrl

        print(f'No working URL found for media {sitemapUrl}')
        return False
    else:
        print('Failed to retrieve sitemap from', sitemapUrl)
        return False


def checkIfDateValid(realDate):
    try:
        date = datetime.strptime(realDate, '%Y-%m-%dT%H:%M:%SZ')
        date = date.replace(tzinfo=pytz.UTC)
        currentDate = datetime.utcnow().replace(tzinfo=pytz.UTC)
        invalidDate = currentDate - timedelta(days=60)
        if invalidDate <= date <= currentDate:
            print('Valid date found')
            return True
        else:
            print('Date is either 2 months old or in the future')
            return False
    except ValueError:
        print('Incorrect date format, check is skipped')
        return None



    """
Parse sitemaps, check if <news:news> is present on sitemap, +
else flag it as False, +
put <loc> into variable, +
#TODO
if no <loc> check if <sitemap> is present,
try opening <sitemap>,
if no <sitemap> – invalid media,
repeat func,
if <loc> is present check if <lastmod> or <news:publication_date> is present,
check if publication date is not older than 2 months ago,
check if <news:language> is present. If not – flag = False.

Check if metatags are present on webpage:
a) og:type content: article,
b) og:locale OR html/lang OR Content-Type = "en",
/// if both are not present – check if <news:language> flag is True, if not – media invalid.
    """
