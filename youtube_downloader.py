import sys

import youtube_dl

def download(url):
    with youtube_dl.YoutubeDL() as ydl:
        ydl.download(url)

if __name__ == "__main__":
    # if(len(sys.argv) < 2):
    #     print("Please specify artist artist and title.")
    #     print("E.g: python3 youtube_downloader.py \"Jousboxx, Fyrebreak, Joelle J\" \"Beyond\"")
    #     exit()

    # artist = sys.argv[1]
    # title = sys.argv[2]

    print(sys.argv[1])

    download(sys.argv[1])