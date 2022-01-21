import sys
import requests
from bs4 import BeautifulSoup

def get_lyrics_azlyrics(artist, title):
    search_results_page_response = requests.get(f'https://search.azlyrics.com/search.php?q={artist}+{title}')

    search_html = search_results_page_response.text

    # Get the HTML of the search results page into BeautifulSoup
    soup = BeautifulSoup(str(search_html), 'html.parser')

    # Find anchor tags
    anchors = soup.find_all('a')
    
    lyrics_page_url = ""

    for anchor in anchors:
        # Valid links to lyrics pages have format like '1. "Breathe" - Mako'. All other a tags don't have periods.
        if("." in anchor.text):
            lyrics_page_url = anchor['href']

    print(lyrics_page_url)

if(len(sys.argv) < 2):
    print("Please specify artist artist and title.")
    print("E.g: python3 lyric_getter.py \"Jousboxx, Fyrebreak, Joelle J\" \"Beyond\"")
    exit()

artist = sys.argv[1]
title = sys.argv[2]

print(f"Artist: {artist}, Title: {title}")

get_lyrics_azlyrics(artist, title)
