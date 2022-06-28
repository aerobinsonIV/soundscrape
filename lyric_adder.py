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

if __name__ == "__main__":
    add_lyrics("trippp3.mp3", "poggers\nweufbwieufbwiuefbwiefbu\nweofwubireubergergergeg")