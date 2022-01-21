import sys
import requests

def get_lyrics_azlyrics(artist, title):
    x = requests.get(f'https://search.azlyrics.com/search.php?q={artist}+{title}')

    print(x.text)

if(len(sys.argv) < 2):
    print("Please specify artist artist and title.")
    print("E.g: python3 lyric_getter.py \"Jousboxx, Fyrebreak, Joelle J\" \"Beyond\"")
    exit()

artist = sys.argv[1]
title = sys.argv[2]

print(f"Artist: {artist}, Title: {title}")

get_lyrics_azlyrics(artist, title)
