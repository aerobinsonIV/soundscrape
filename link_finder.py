import requests
from bs4 import BeautifulSoup

from soup_url import soup_url

def soundcloud(artist, title):
    search_soup = soup_url(f'https://soundcloud.com/search?q={artist}%20{title}')

    # results_list = search_soup.find_all(class_="searchItem")

    # print(results_list)

    print(search_soup)


soundcloud("fyrebreak", "beyond")