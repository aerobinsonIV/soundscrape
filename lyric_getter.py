import sys
import requests

if(len(sys.argv) < 2):
    print("Please specify artist artist and title.")
    print("E.g: python3 lyric_getter.py \"Jousboxx, Fyrebreak, Joelle J\" \"Beyond\"")
    exit()

artist = sys.argv[1]
title = sys.argv[2]

print(f"Artist: {artist}, Title: {title}")


x = requests.get('https://w3schools.com')
print(x.text)