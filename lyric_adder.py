import os
import sys

from lyric_getter import clean_artist, clean_title, get_lyrics_genius
sys.path.insert(0, os.path.join(os.getcwd(), "stagger"))
import stagger
from stagger.id3 import *
from metadata_scanner import scan_file

def add_lyrics(song_file, lyrics):

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

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Please specify a file or folder.")
        exit()
    filenames = []

    if os.path.isfile(sys.argv[1]):
        # This is a single file
        filenames.append(sys.argv[1])

    elif os.path.isdir(sys.argv[1]):
        dir_list = os.listdir(sys.argv[1])
        for file in dir_list:
            filenames.append(os.path.join(sys.argv[1], file))

    print("About to process the following files:")
    for filename in filenames:
        print(filename)

    for filename in filenames:

        scanned_title, scanned_artist = scan_file(filename)
        cleaned_title = clean_title(scanned_title)
        cleaned_artist = clean_artist(scanned_artist)

        # If one song fails, just ignore it and keep going
        try:
            
            lyrics = get_lyrics_genius(cleaned_artist, cleaned_title)

            edited_lyrics = notepad(cleaned_artist, cleaned_title, lyrics)

            add_lyrics(filename, edited_lyrics)
        except:
            print(f"Failed to retrieve lyrics for {scanned_artist} - {scanned_title}.")