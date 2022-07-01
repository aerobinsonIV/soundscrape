import os
import sys

from lyric_getter import get_lyrics_azlyrics, get_lyrics_genius
sys.path.insert(0, os.path.join(os.getcwd(), "stagger"))
import stagger
from stagger.id3 import *
from metadata_scanner import scan_file

def add_lyrics(song_file, lyrics):

    # Open tag on song file
    tag = stagger.read_tag(song_file)
    
    tag['USLT'] = "eng|" + lyrics
    tag.write(song_file)

def notepad(lyrics):

    lyric_file_path = os.path.join(os.path.join(os.getcwd(), "temp"), "lyrics.txt")

    with open(lyric_file_path, "w", encoding='utf8') as f:
        f.write(lyrics)

    # move along hackers, nothing to see here
    os.system("notepad " + lyric_file_path)

    with open(lyric_file_path, "r", encoding='utf8') as f:
        edited_lyrics = f.read()

    os.remove(lyric_file_path)

    return(edited_lyrics)

if __name__ == "__main__":
    # Check args
    # Open file/scan metadata
    # Get lyrics for that artist/title
    # Notepad the lyrics
    # Write lyrics to file

    if(len(sys.argv) < 1):
        print("Please specify a file.")
        exit()

    filename = sys.argv[1]
    scanned_title, scanned_artist = scan_file(filename)
    
    lyrics = get_lyrics_genius(scanned_artist, scanned_title)

    edited_lyrics = notepad(lyrics)

    print(f"Edited lyrics: {edited_lyrics}")

    add_lyrics(filename, edited_lyrics)