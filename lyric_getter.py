import sys
from bs4 import BeautifulSoup
from bs4 import Comment
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

LYRICS_CONTAINER_CLASS = "Lyrics__Container-sc-1ynbvzw-6 YYrds"

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

def get_html_genius(artist, title, filename = None):
     # Make input case insensitive
    artist = artist.lower()
    title = title.lower()

    search_soup = soup_url(f'https://genius.com/search?q={artist}+{title}')

    driver = webdriver.Firefox()

    driver.get(f'https://genius.com/search?q={artist}+{title}')
    time.sleep(1)

    # result_labels = driver.find_elements(By.CLASS_NAME, "search_results_label")
    result_sections = driver.find_elements(By.TAG_NAME, "search-result-section")

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

    if filename != None:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(lyrics_page_html)

    return lyrics_page_html

def extract_lyrics_from_html_genius(html):

    lyrics_soup = BeautifulSoup(str(html), 'html.parser')
    # Find div tags
    lyrics_divs = lyrics_soup.find_all(class_=LYRICS_CONTAINER_CLASS)

    lyrics_divs_no_brackets_str = ""

    for div in lyrics_divs:
        # Remove square bracket sections (e.g. [Verse 1: Mitchel Cave]) by converting to string, applying regex substitution, then converting back to soup
        # https://stackoverflow.com/a/14599280
        lyrics_divs_no_brackets_str += re.sub("[\[].*?[\]]", "\n", str(div))
    
    soup_list = BeautifulSoup(lyrics_divs_no_brackets_str, 'html.parser').contents

    all_lyrics = ""

    # Loop through each top-level lyrics div (usually one or a few)
    for soup in soup_list:
        all_lyrics += genius_parse_helper(soup)

    return all_lyrics

def genius_parse_helper(input_soup):
    contents = input_soup.contents
    lyrics = ""
    last_item_break = False
    last_line_break = False

    for item in contents:

        if item.name == "a":
            # This is an annotated section, comprised of a span wrapped in an anchor tag
            # Get inside the anchor and recurse into the span
            processed = genius_parse_helper(item.contents[0])
            
            if len(processed) == 1:
                # Probably just a line break, pretend we never saw this
                continue

            # Trim out extra line break(s) that somehow sneak onto end of every annotated section. Leave the last one.
            while len(processed) > 1 and processed[-1] == "\n":
                processed = processed[:-1]

            for line in processed.split("\n"):
                if len(line) > 1:
                    lyrics += line + "\n"
            
        elif item.name == "i":
            # Recurse into the italicized section
            processed = genius_parse_helper(item)
            lines = processed.split("\n")

            # If a lyric section is italicized, it's probably background/reverbed vocals.
            # Since we can't italicize plaintext, we instead represent this effect by wrapping the lyrics in parens.
            with_parens = ""
            for line in lines:
                # Ignore lines that are already parenthesized and lines that are just newlines
                if len(line) > 1 and line[0] != "(":
                    with_parens += f"({line})\n"
            lyrics += with_parens
        elif item.name == "br":

            # Put down one line break if two are encountered in a row in the HTML (because the first is just used to terminal lines on the site)
            # Don't do two consecutive emtpy lines in the output
            if not last_line_break:
                if last_item_break:
                    lyrics += "\n"
                    last_line_break = True
                else:
                    last_item_break = True
            continue

        elif item.name == "span" or item.name == "div":
            pass
        else:
            # Disregard single parens, these usually occur before italicized sections which will be parenthesized anyway
            if str(item) != "(" and str(item) != ")":
                if str(item) == "\n":
                    if not last_line_break:
                        lyrics += "\n"
                        last_line_break = True
                        continue
                else:
                    # Also look for single parens at the start and end of a text line, because the paren could be directly adjacent to an italicized element
                    if str(item)[-1] == "(":
                        lyrics += str(item)[:-1] + "\n"
                    elif str(item)[1] == ")":
                        lyrics += str(item)[1:] + "\n"
                    else:
                        lyrics += str(item) + "\n"
        
        last_item_break = False
        last_line_break = False
    
    # Trim excess newlines off start and end
    if lyrics[0] == "\n":
        lyrics = lyrics[1:]

    while len(lyrics) > 1 and lyrics[-1] == "\n":
            lyrics = lyrics[:-1]

    # these irrationally bother me
    lyrics = re.sub("'Cause", "Cause", lyrics)
    lyrics = re.sub("'cause", "cause", lyrics)

    lyrics = re.sub("I'mma", "Imma", lyrics)
    lyrics = re.sub("i'mma", "imma", lyrics)

    lyrics = re.sub("I'ma", "Imma", lyrics)
    lyrics = re.sub("i'ma", "imma", lyrics)

    lyrics = re.sub("’", "'", lyrics)
    lyrics = re.sub("‘", "'", lyrics)

    lyrics = re.sub("“", '"', lyrics)
    lyrics = re.sub("”", '"', lyrics)

    return lyrics

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
    # if(len(sys.argv) < 2):
    #     print("Please specify artist artist and title.")
    #     print("E.g: python3 lyric_getter.py \"Jousboxx, Fyrebreak, Joelle J\" \"Beyond\"")
    #     exit()

    # artist = sys.argv[1]
    # title = sys.argv[2]

    # get_html_genius(artist, title, "call_me_back.html")

    with open("call_me_back.html", 'r', encoding='utf-8') as f:
        # extract_lyrics_from_html_genius(f.read())
        print(extract_lyrics_from_html_genius(f.read()))

    # print(extract_lyrics_from_html_genius(artist, title))
