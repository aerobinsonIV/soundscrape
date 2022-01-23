import requests
from bs4 import BeautifulSoup

from soup_url import soup_url

def soundcloud(artist, title):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
    }

    search_soup = soup_url(f'https://soundcloud.com/search?q={artist}%20{title}', headers)

    # results_list = search_soup.find_all(class_="searchItem")

    # print(results_list)

    print(search_soup)

    


soundcloud("fyrebreak", "beyond")