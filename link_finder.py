import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def soundcloud(artist, title):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
    }

    search_url = f'https://soundcloud.com/search?q={artist}%20{title}'

    driver = webdriver.Firefox()
    driver.get(search_url)

    


soundcloud("fyrebreak", "beyond")