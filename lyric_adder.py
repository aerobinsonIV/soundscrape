import stagger
from stagger.id3 import *
import os

# Will assume file with name song_file is in the temp/ folder
def add_lyrics(song_file, lyrics):
    path = os.path.join(os.getcwd(), "temp")

    # Open tag on song file
    # tag = stagger.read_tag(os.path.join(path, song_file))
    
    # Create new tag
    tag = stagger.Tag23()
    
    # UnSynchronized Lyrics/Text
    tag[USLT] = lyrics
    # tag[TPE1] = lyrics
    tag.write(os.path.join(path, song_file))

if __name__ == "__main__":
    add_lyrics("trippp3.mp3", "poggers")