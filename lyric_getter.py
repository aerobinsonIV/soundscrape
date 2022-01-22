import sys
import requests
from bs4 import BeautifulSoup
from bs4 import Comment

def get_lyrics_azlyrics(artist, title):
    search_results_page_response = requests.get(f'https://search.azlyrics.com/search.php?q={artist}+{title}')

    search_html = search_results_page_response.text

    # Get the HTML of the search results page into BeautifulSoup
    search_soup = BeautifulSoup(str(search_html), 'html.parser')

    # Find anchor tags
    anchors = search_soup.find_all('a')
    
    lyrics_page_url = ""

    for anchor in anchors:
        # Valid links to lyrics pages have format like '1. "Breathe" - Mako'. All other a tags don't have periods.
        if("." in anchor.text):
            lyrics_page_url = anchor['href']

    # Get lyrics page
    lyrics_page_response = requests.get(lyrics_page_url)

    lyrics_html = lyrics_page_response.text

    lyrics_soup = BeautifulSoup(str(lyrics_html), 'html.parser')

    # The lyrics section is a div.
    divs = lyrics_soup.find_all('div')

    # The div containing the lyric starts with this comment
    licensing_comment_text = ' Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. '
    
    most_breaks = 0
    most_breaks_index = 0
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


if(len(sys.argv) < 2):
    print("Please specify artist artist and title.")
    print("E.g: python3 lyric_getter.py \"Jousboxx, Fyrebreak, Joelle J\" \"Beyond\"")
    exit()

artist = sys.argv[1]
title = sys.argv[2]

print(f"Artist: {artist}, Title: {title}")

print(get_lyrics_azlyrics(artist, title))
