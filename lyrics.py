import os
import sys
import re #regex 
from fuzzywuzzy import fuzz # Fuzzy string matching library

# Import modified stagger submodule
sys.path.insert(0, os.path.join(os.getcwd(), "stagger"))
import stagger
from stagger.id3 import *

def match_confidence(real_title, real_artist, test_title, test_artist):
    title_ratio = fuzz.ratio(real_title.lower(), test_title.lower())
    artist_ratio = fuzz.ratio(real_artist.lower(), test_artist.lower())

    # Exclude results that are very certainly wrong
    if title_ratio < 50:
        title_ratio = 0

    if artist_ratio < 50:
        artist_ratio = 0

    return artist_ratio + title_ratio

def search_term_preprocessing(input_string):
    return input_string.replace("&", "%26").lower()
    
def clean_title(title):

    # https://medium.com/@georgelgore/using-regex-to-remove-brackets-and-parentheses-from-a-string-3a6067155d74

    no_parens = re.sub("\(.*\)", "", title)
    no_brackets = re.sub("\[.*\]", "", no_parens)
    no_ft = no_brackets.split("ft.")[0]
    no_feat = no_ft.split("feat.")[0]
    no_Feat = no_feat.split("Feat.")[0]

    return no_Feat.strip()

def clean_artist(artist):
    no_semicolons = artist.replace(";", "")
    no_commas = no_semicolons.replace(",", "")
    return no_commas.strip()

def add_lyrics_to_song_file(song_file, lyrics):

    # Lyrics are probably in utf-8, so encode them into ascii so my hacky stagger hack doesn't flip out
    ascii_lyrics = lyrics.encode("ascii", "ignore")

    # Open tag on song file
    tag = stagger.read_tag(song_file)
    
    tag['USLT'] = "eng|" + ascii_lyrics.decode()
    tag.write(song_file)

def gen_filename_helper(input_string):
    illegal_chars = ["\"", "*", "/", ":", "<", ">", "?", "\\", "|"]
    processed_string = input_string.strip()

    for char in illegal_chars:
        processed_string = processed_string.replace(char, "")

    return processed_string.replace(" ", "_").lower()

def generate_lyrics_filename(artist, title):

    cleaned_artist = gen_filename_helper(artist)
    cleaned_title = gen_filename_helper(title)

    filename = f"{cleaned_artist}_{cleaned_title}.txt"

    return filename

def notepad(artist, title, lyrics):

    lyric_filename = generate_lyrics_filename(artist, title)
    lyric_file_path = os.path.join(os.path.join(os.getcwd(), "temp"), lyric_filename)

    with open(lyric_file_path, "w", encoding='utf8') as f:
        f.write(lyrics)

    # move along hackers, nothing to see here
    os.system(f"notepad \"{lyric_file_path}\"")

    with open(lyric_file_path, "r", encoding='utf8') as f:
        edited_lyrics = f.read()

    os.remove(lyric_file_path)

    return(edited_lyrics)

