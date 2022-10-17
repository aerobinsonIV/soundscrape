import argparse
import os

def get_yt_music_metadata(link: str):
    return ("twewt", "wefwfe", "ewfwefwf", "fffffff")

def youtube_dl_wrapper(link: str, transcode_to_mp3: bool = False, cover_artwork: bool = False, music: bool = False):
    
    TITLE_XPATH = "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/yt-formatted-string"
    ARTIST_XPATH = "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/span/span[2]/yt-formatted-string/a[1]"
    ALBUM_XPATH = "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/span/span[2]/yt-formatted-string/a[2]"
    YEAR_XPATH = "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/span/span[2]/yt-formatted-string/span[3]"

    args = "--extract-audio "
    if transcode_to_mp3:
        args += "--audio-format mp3 --audio-quality 128k "
    
    if cover_artwork:
        args += "--embed-thumbnail "

    os.system("youtube-dl" + " " + args + " " + link)

    if music:
        print("Got music param")
        print(get_yt_music_metadata(link))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="YouTube link or path of a file containing a list of YouTube links")
    parser.add_argument("-t", "--transcode-to-mp3", help="Transcode the downloaded opus file to mp3, lower quality but better compatibility", action='store_true')
    parser.add_argument("-c", "--cover-artwork", help="Embed video thumbnail as cover artwork", action='store_true')
    parser.add_argument("-m", "--music", help="Treat this as a YouTube music link (rather than e.g. a music video) and get the title, artist, and year from the webpage.", action='store_true')
    
    args = parser.parse_args()

    print(args.target)

    # Download songs to the temp folder
    os.chdir("./temp")

    if args.target[:7] == "http://" or args.target[:8] == "https://" or args.target[:4] == "www.":
        # URL
        youtube_dl_wrapper(args.target, args.transcode_to_mp3, args.cover_artwork, args.music)
    else:
        # Path to file containing list of links
        with open(args.target, 'r') as f:
            lines = f.readlines()

        for line in lines:
                print(f"Downloading {line}", end="")
                youtube_dl_wrapper(line, args.transcode_to_mp3, args.cover_artwork, args.music)
