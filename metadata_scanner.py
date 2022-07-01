import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), "stagger"))
import stagger
from stagger.id3 import *

def scan_file(filename):
    # Open tag on song file
    tag = stagger.read_tag(filename)

    title = tag['TIT2'].text[0]
    artist = tag['TPE1'].text[0]

    return (title, artist)

if __name__ == "__main__":
    if(len(sys.argv) < 1):
        print("Please specify a file.")
        exit()

    filename = sys.argv[1]
    data = scan_file(filename)
    print(f"This file contains the song {data[0]} by {data[1]}.")