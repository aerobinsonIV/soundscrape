import os
from string import punctuation
import sys
from bs4 import BeautifulSoup
from bs4 import Comment
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import re #regex 
from fuzzywuzzy import fuzz # Fuzzy string matching library

from soup_url import soup_url

LYRICS_CONTAINER_CLASS = "Lyrics__Container-sc-1ynbvzw-6 YYrds"

def match_confidence(real_title, real_artist, test_title, test_artist):
    title_ratio = fuzz.ratio(real_title, test_title)
    artist_ratio = fuzz.ratio(real_artist, test_artist)

    # Exclude results that are very certainly wrong
    if title_ratio < 50:
        title_ratio = 0

    if artist_ratio < 50:
        artist_ratio = 0

    return artist_ratio + title_ratio

def search_term_preprocessing(input_string):
    return input_string.replace("&", "%26")

def get_html_genius(artist, title, cache = False):
    # Make input case insensitive
    artist = artist.lower()
    title = title.lower()

    cache_path = os.path.join(os.getcwd(), "cached_html")
    cache_filename = re.sub(" ", "_", artist) + "_" + re.sub(" ", "_", title) + "_genius.html"
    cache_full_path = os.path.join(cache_path, cache_filename)
    
    # Does cache dir exist?
    if os.path.isdir(cache_path):

        # Is the HTML for this particular song cached?
        if os.path.isfile(cache_full_path):
            with open(cache_full_path, "r", encoding="utf-8") as f:
                html = f.read()
            
            print(f"Found HTML for {artist} - {title} in cache!")
            return html
    else:
        os.mkdir(cache_path)

    processed_artist = search_term_preprocessing(artist)
    processed_title = search_term_preprocessing(title)

    driver = webdriver.Firefox()
    
    ublock_origin_path = "ublock_origin-1.43.0.xpi"
    driver.install_addon(ublock_origin_path)
    
    driver.get(f'https://genius.com/search?q={processed_artist}+{processed_title}')

    wait_for_section = WebDriverWait(driver, 180)
    wait_for_section.until(expected_conditions.presence_of_element_located((By.TAG_NAME, "search-result-section")))
    result_sections = driver.find_elements(By.TAG_NAME, "search-result-section")

    wait_for_label = WebDriverWait(driver, 180)
    wait_for_label.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "search_results_label")))
    for item in result_sections:
        try:
            result_label = item.find_element(By.CLASS_NAME, "search_results_label")
            if result_label.get_attribute('innerHTML') == "Songs":
                song_results_section_html = item.get_attribute('innerHTML')
                break
        except:
            # This page is weird and not all the results sections have this label
            continue
    
    driver.close()

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

    # Get lyrics page from link that best matched input title and artist
    lyrics_page_soup = soup_url(best_url)

    lyrics_page_html = str(lyrics_page_soup.prettify())

    # Cache HTML for this song
    if cache:
        with open(cache_full_path, "w", encoding="utf-8") as f:
            f.write(lyrics_page_html)

    return lyrics_page_html

def remove_newlines(input_string):
    # Remove extra backslashes preceding newlines
    no_leading_slashes_newlines = re.sub("\\\\+\n", "\n", re.sub("\\\\+n", "\n", str(input_string)))

    # Remove newlines
    return re.sub("\n", "", no_leading_slashes_newlines)

def genius_parse_preprocessing(input_string: str):
    no_newlines = remove_newlines(input_string)

    # Remove square bracket sections (e.g. [Verse 1: Mitchel Cave]) by converting to string, applying regex substitution, then converting back to soup
    # https://stackoverflow.com/a/14599280
    return re.sub("[\[].*?[\]]", "", str(no_newlines))

def extract_lyrics_from_html_genius(html):

    lyrics_soup = BeautifulSoup(str(html), 'html.parser')
    # Find div tags
    lyrics_divs = lyrics_soup.find_all(class_=LYRICS_CONTAINER_CLASS)

    lyrics_divs_preprocessed_str = ""

    for div in lyrics_divs:
        lyrics_divs_preprocessed_str += genius_parse_preprocessing(div)
    
    soup_list = BeautifulSoup(lyrics_divs_preprocessed_str, 'html.parser').contents

    all_lyrics = ""

    # Loop through each top-level lyrics div (usually one or a few)
    for soup in soup_list:
        all_lyrics += genius_parser(soup)
        # all_lyrics += "\n\n" # Divs occur on lyrical sections so put in a blank line for nice spacing

    all_lyrics = all_lyrics.strip()
    return all_lyrics

def genius_parser(input_soup):
    contents = input_soup.contents
    lyrics = "" # This will be stripped out anyway and it makes more consistent functionality for divs that don't begin with <br>
    num_consecutive_breaks = 0
    in_parens = False

    for i, item in enumerate(contents):

        if item.name == "a":
            # This is an annotated section, comprised of a span wrapped in an anchor tag
            # Get inside the anchor, find and recurse into the span (there might be \n, <br>, or other junk to skip)
            for sub_item in item.contents:
                if sub_item.name == "span":
                    processed = genius_parser(sub_item)
                    break
            
            if len(processed.strip()) == 0:
                # If this is a dud, skip resetting break counter
                continue

            if len(lyrics) > 1 and lyrics[-1] != "\n":
                # This is an inline annotation, throw in a whitespace to compensate for the stripping
                lyrics += " "

            lyrics += processed

        elif item.name == "i":
            processed = genius_parser(item)
            if in_parens:
                lyrics += f"{processed.strip()}"
            else:
                lyrics += f"({processed.strip()})"

        elif item.name == "b":
            processed = genius_parser(item)

            if len(lyrics) > 1 and lyrics[-1] != "\n":
                # This is an inline annotation, throw in a whitespace to compensate for the stripping
                lyrics += " "

            lyrics += f"{processed.strip()}"

        elif item.name == "br":
            if num_consecutive_breaks < 2:
                lyrics += "\n"
                num_consecutive_breaks += 1
            continue

        elif item.name == "span" or item.name == "div": # Probably an ad or something else we don't care about
            continue
        
        else:
            stripped_item = str(item).strip()
            if len(stripped_item) > 0:
                
                # Implicitly trusting Genius not to go more than one parens deep to avoid having to do full-blown tokenization or whatever
                if in_parens:
                    if ")" in stripped_item and "(" not in stripped_item:
                        in_parens = False
                else:
                    if "(" in stripped_item and ")" not in stripped_item:
                        in_parens = True

                # If we're adding on to an existing line (e.g. because of an inline annotation followed by non-annotated lyrics), insert whitespace to compensate for stripping
                if len(lyrics) > 1 and lyrics[-1] != "\n":
                    lyrics += " "
                    pass

                lyrics += stripped_item
            else:
                continue
    
        num_consecutive_breaks = 0

    # Post-processing

    # Sometimes italicized sections are wrapped in parens. Since we parenthesize all italics, that could result in double parens. Remove those.
    lyrics = lyrics.replace("((", "(")
    lyrics = lyrics.replace("))", ")")

    # Adding spaces after annotations could result in a space between text and a punctuation mark.
    # Since there's no legitimate reason for a space there, we can just fix it with a substitution.
    punctuations = [",", ".", "!", "?", ":", ";", "/", "\\", "%", "}", ")"]
    for punctuation in punctuations:
        lyrics = lyrics.replace(f" {punctuation}", punctuation)

    lyrics = lyrics.replace("{ ", "{") # super edge case this will probably never happen

    lyrics = lyrics.replace("I'mma", "Imma")
    lyrics = lyrics.replace("i'mma", "imma")

    lyrics = lyrics.replace("I'ma", "Imma")
    lyrics = lyrics.replace("i'ma", "imma")

    lyrics = lyrics.replace("’", "'")
    lyrics = lyrics.replace("‘", "'")
    lyrics = lyrics.replace("“", '"')
    lyrics = lyrics.replace("”", '"')

    lyrics = lyrics.replace("'Cause", "Cause")
    lyrics = lyrics.replace("'cause", "cause")

    lyrics = lyrics.replace("'Tryna", "Tryna")
    lyrics = lyrics.replace("'tryna", "tryna")

    lyrics = lyrics.replace("n' ", "ng ")
    lyrics = lyrics.replace("N' ", "NG ")
    lyrics = lyrics.replace("n'\n", "ng\n")
    lyrics = lyrics.replace("N'\n", "NG\n")
    lyrics = lyrics.replace("n')", "ng)")
    lyrics = lyrics.replace("N')", "NG)")

    return lyrics

def get_lyrics_genius(artist, title, cache=False):
    html = get_html_genius(artist, title, cache)
    return extract_lyrics_from_html_genius(html)

def get_lyrics_azlyrics(artist, title):

    search_soup = soup_url(f'https://search.azlyrics.com/search.php?q={artist}+{title}')
    
    # Find bold tags
    bolds = search_soup.find_all('b')

    for bold in bolds:
        # Song results pane is labelled by a b tag with this text
        if bold.text == "Song results:":
            song_results_pane = bold.parent.parent
            break
        
    if not ('song_results_pane' in locals()):
        # Couldn't find this song
        return None

    # Find anchor tags
    anchors = song_results_pane.find_all('a')

    found_result = False
    best_confidence = 0

    for anchor in anchors:
        # Valid links to lyrics pages have format like '1. "Breathe" - Mako'. All other a tags don't have periods.
        if("." in anchor.text):

            # just be happy it's not regex
            a_title = anchor.text[4:anchor.text[4:].find("\"") + 4].strip().lower()
            a_artist = anchor.text[anchor.text[1:].find("-") + 3:].strip().lower()

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

    # Since this script is being run standalone rather than having its functions called by lyric_adder,
    # We're most likely debugging. Cache HTML files so we don't have to keep redownloading them
    # If we're debugging parsing.
    print(get_lyrics_genius(artist, title, cache=True))
