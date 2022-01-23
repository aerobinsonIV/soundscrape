import requests
from bs4 import BeautifulSoup

# Take in a URL and return a beautifulSoup object of the page
def soup_url(url):
    response = requests.get(url)

    html = response.text

    return BeautifulSoup(str(html), 'html.parser')