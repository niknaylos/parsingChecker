import requests
import re
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import pytz
from dateutil import parser


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
        newsTags = soup.find_all('news:news')
        if newsTags:
            # print(f'Tag <news:news> found in sitemap at {sitemapUrl}')
            return True
        else:
            # print(f'Tag <news:news> not found in sitemap at {sitemapUrl}')
            return False
    else:
        print(f'Failed to retrieve sitemap from {sitemapUrl}. Status code: {response.status_code}')
        return False


def newsLangExists(sitemapUrl):
    if newsTagExists(sitemapUrl):
        response = makeRequest(sitemapUrl)
        soup = bs(response.content, 'xml')
        langTag = soup.find_all('news:language')
        if langTag:
            print(f'found news:language on sitemap')
            return True
        else:
            print(f'news:language is not found')
            return False


def newsArticleLang(url):
    response = makeRequest(url)
    if response:
        soup = bs(response.content, 'html.parser')
        og_locale_tag = soup.find('meta', {'property': 'og:locale'})
        if og_locale_tag:
            print(f"Meta tag og:locale found with content '{og_locale_tag['content']}'.")
            return True
        else:
            print(f"Meta tag og:locale not found.")

        # Check for html lang attribute
        html_lang_tag = soup.find('html', lang=True)
        if html_lang_tag:
            print(f"HTML lang attribute found with value '{html_lang_tag['lang']}'.")
            return True
        else:
            print(f"HTML lang attribute not found.")

        # Check for Content-Type meta tag
        content_type_tag = soup.find('meta', {'http-equiv': 'Content-Type'})
        if content_type_tag:
            print(f"Meta tag Content-Type found with content '{content_type_tag['content']}'.")
            return True
        else:
            print(f"Meta tag Content-Type not found.")
            return False
    else:
        print(f"Failed to retrieve the webpage. HTTP Status Code: {response.status_code}")
        return False

def publicationDateExists(sitemapUrl):
    response = makeRequest(sitemapUrl)
    if response:
        soup = bs(response.content, 'xml')
        lastMod = soup.find_all('lastmod')
        pubDate = soup.find_all('news:publication_date')
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
        date = parser.parse(realDate)
    except ValueError:
        print('Incorrect date format, check is skipped')
        return None

    # Ensure the date is in UTC timezone
    date = date.astimezone(pytz.UTC)
    currentDate = datetime.utcnow().replace(tzinfo=pytz.UTC)
    invalidDate = currentDate - timedelta(days=60)

    if invalidDate <= date:
        print('Valid date found')
        if date > currentDate:
            print(f'date could be in the future')
        return True
    else:
        print('Date could be 2 months old')
        return False


def checkType(url):
    response = makeRequest(url)
    if response:
        soup = bs(response.content, 'html.parser')

        # Check for og:type meta tag with content set to article
        og_type_tag = soup.find('meta', {'property': 'og:type', 'content': 'article'})
        if og_type_tag:
            print(f"Meta tag og:type with content 'article' found.")
            return True
        else:
            print(f"Meta tag og:type with content 'article' not found.")
            return False
    else:
        print(f"Failed to retrieve the webpage. HTTP Status Code: {response.status_code}")
        return False
