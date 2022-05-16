import sys
import requests
from bs4 import BeautifulSoup
from bs4 import Comment
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from fuzzywuzzy import fuzz # Fuzzy string matching library

from soup_url import soup_url

def match_confidence(real_title, real_artist, test_title, test_artist):
    title_ratio = fuzz.ratio(real_title, test_title)
    artist_ratio = fuzz.ratio(real_artist, test_artist)

    # Exclude results that are very certainly wrong
    if title_ratio < 50:
        title_ratio = 0

    if artist_ratio < 50:
        artist_ratio = 0

    return artist_ratio + title_ratio

def get_lyrics_genius(artist, title):
    
    # Make input case insensitive
    artist = artist.lower()
    title = title.lower()

    # PageHeaderSearchdesktop__Input-eom9vk-2 gajVFV
    # search_soup = soup_url(f'https://genius.com/search?q={artist}+{title}')

    # print(search_soup)

    # driver = webdriver.Firefox()

    # driver.get(f'https://genius.com/search?q={artist}+{title}')
    # time.sleep(1)

    # # result_labels = driver.find_elements(By.CLASS_NAME, "search_results_label")
    # result_sections = driver.find_elements(By.TAG_NAME, "search-result-section")

    # for item in result_sections:
    #     try:
    #         result_label = item.find_element(By.CLASS_NAME, "search_results_label")
    #         if result_label.get_attribute('innerHTML') == "Songs":
    #             song_results_section_html = item.get_attribute('innerHTML')
    #             break
    #     except:
    #         # This page is weird and not all the results sections have this label
    #         continue
    
    # driver.close()

    with open("song_results_section.html", "r", encoding="utf-8") as f:
        song_results_section_html = f.read() 

    search_soup = BeautifulSoup(song_results_section_html, 'html.parser')

    anchors = search_soup.find_all(class_='mini_card')

    found_result = False
    best_confidence = 0

    for anchor in anchors:

        a_title = anchor.find_all(class_='mini_card-title')[0].text.strip().lower()
        a_artist = anchor.find_all(class_='mini_card-subtitle')[0].text.strip().lower()

        confidence = match_confidence(title, artist, a_title, a_artist)
        if confidence > best_confidence:
            best_url = anchor['href']
            best_confidence = confidence
        
        # We found at least one result
        found_result = True

    if not found_result:
        return None

    if best_confidence == 0:
        # None of the results were even close
        return None

    print(best_url)

    # # Get lyrics page from link that best matched input title and artist
    # lyrics_soup = soup_url(best_url)

    # Search_soup is useless here, we need to use selenium to run Javascript

    # Class of lyrics div is "Lyrics__Container-sc-1ynbvzw-6 jYfhrf"

    # # Find div tags
    # divs = search_soup.find_all('div')

    # for div in divs:
    #     # Song results pane is labelled by a div tag with this text
    #     if div.text == "Songs":
    #         song_results_pane = div.parent
    #         break
    
    # print(song_results_pane)

def get_lyrics_azlyrics(artist, title):

    search_soup = soup_url(f'https://search.azlyrics.com/search.php?q={artist}+{title}')
    
    # Find bold tags
    bolds = search_soup.find_all('b')

    for bold in bolds:
        # Song results pane is labelled by a b tag with this text
        if bold.text == "Song results:":
            song_results_pane = bold.parent.parent
            break

    # Find anchor tags
    anchors = song_results_pane.find_all('a')

    found_result = False
    best_confidence = 0

    for anchor in anchors:
        # Valid links to lyrics pages have format like '1. "Breathe" - Mako'. All other a tags don't have periods.
        if("." in anchor.text):

            # just be happy it's not regex
            a_title = anchor.text[4:anchor.text[4:].find("\"") + 4]
            a_artist = anchor.text[anchor.text[1:].find("-") + 3:]

            confidence = match_confidence(title, artist, a_title, a_artist)
            if confidence > best_confidence:
                best_url = anchor['href']
                best_confidence = confidence
            
            # We found at least one result
            found_result = True

    if not found_result:
        return None

    if best_confidence == 0:
        # None of the results were even close
        return None

    # Get lyrics page from link that best matched input title and artist
    lyrics_soup = soup_url(best_url)

    # The lyrics section is a div.
    divs = lyrics_soup.find_all('div')

    # The div containing the lyric starts with this comment
    licensing_comment_text = ' Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. '
    
    for i, div in enumerate(divs):
        
        # Get all comments in this div
        comments = div.find_all(string=lambda text: isinstance(text, Comment))
        
        # If the div has a comment, it might be our target div
        if(len(comments) > 0):
            # Check if the first comment is the licensing warning
            if(comments[0] == licensing_comment_text):
                
                divs_in_lyric_div_candidate = div.find_all('div')

                # The lyrics div has no divs nested inside it
                if(len(divs_in_lyric_div_candidate) == 0):
                    # If we've passed all these tests, we definetly have the lyrics
                    return div.text.strip()

    return ""

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Please specify artist artist and title.")
        print("E.g: python3 lyric_getter.py \"Jousboxx, Fyrebreak, Joelle J\" \"Beyond\"")
        exit()

    artist = sys.argv[1]
    title = sys.argv[2]

    # print(f"Artist: {artist}, Title: {title}")

    get_lyrics_genius(artist, title)
