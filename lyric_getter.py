import sys
import requests

def get_lyrics_azlyrics(artist, title){
    x = requests.get(f'https://search.azlyrics.com/search.php?q={artist}+{title}')

    # Dictionary of headers
    # Lifted from Firefox to trick AZLyrics into thinking we're not hackers
    headers = {
        "Host": "search.azlyrics.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.azlyrics.com/",
        "Upgrade-Insecure-Requests": 1,
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }

    x.headers = headers

    print(x.text)
}

if(len(sys.argv) < 2):
    print("Please specify artist artist and title.")
    print("E.g: python3 lyric_getter.py \"Jousboxx, Fyrebreak, Joelle J\" \"Beyond\"")
    exit()

artist = sys.argv[1]
title = sys.argv[2]

print(f"Artist: {artist}, Title: {title}")


