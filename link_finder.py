import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from fuzzywuzzy import fuzz # Fuzzy string matching library
from Levenshtein import distance as lev

def soundcloud(artist, title):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
    }

    search_url = f'https://soundcloud.com/search?q={artist}%20{title}'

    driver = webdriver.Firefox()
    driver.get(search_url)
    print("loaded page")

    # TODO: Change this to detect when the page is loaded and proceed
    time.sleep(3)

    titles = driver.find_element(By.CLASS_NAME, "sc-link-primary")

    # print(titles.text)

    search_list = driver.find_element(By.CLASS_NAME, "searchList").get_attribute("innerHTML")

    # print(search_list)

    search_list_soup = BeautifulSoup(search_list, 'html.parser')

    all_tracks = search_list_soup.find_all(class_="sound")

    for track in all_tracks:
        title_element = track.find(class_="soundTitle__title")
        track_rel_url = title_element['href']
        track_title = title_element.find("span").text.strip()
        track_user = track.find(class_="soundTitle__username").find("span").text.strip()

        print(track_title)
        print(track_user)
        print(track_rel_url)

        print("------------------------------------------------------------------------------------------------")

    driver.close()

def prep_string_for_matching(input):
    return input.lower()

# Function that can parse search results from any website as long as we get them into our standard tuple format:
# (artist/username, title, relative link)
def find_best_match(artist, title, search_results):

    best_match_artist_ratio = 0

    for item in search_results:
        item_artist = item[0]
        item_title = item[1]

        if artist in item_title

soundcloud("i love ", "you")