import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), "stagger"))
import stagger
from stagger.id3 import *

# Will assume file with name song_file is in the temp/ folder
def add_lyrics(song_file, lyrics):
    path = os.path.join(os.getcwd(), "temp")

    # Open tag on song file
    tag = stagger.read_tag(os.path.join(path, song_file))
    
    tag['USLT'] = "eng|" + lyrics
    tag.write(os.path.join(path, song_file))

def notepad(lyrics):

    lyric_file_path = os.path.join(os.path.join(os.getcwd(), "temp"), "lyrics.txt")

    with open(lyric_file_path, "w") as f:
        f.write(lyrics)

    # move along hackers, nothing to see here
    os.system("notepad " + lyric_file_path)

    with open(lyric_file_path, "r") as f:
        edited_lyrics = f.read()

    os.remove(lyric_file_path)

    return(edited_lyrics)

if __name__ == "__main__":
    print(notepad("pee pee poo poo\nweee weee wooo q"))