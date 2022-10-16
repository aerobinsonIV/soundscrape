import argparse
import os

def youtube_dl_wrapper(link: str, transcode_to_mp3: bool = False, cover_artwork: bool = False, music: bool = False):
    
    args = "--extract-audio "
    if transcode_to_mp3:
        args += "--audio-format mp3 --audio-quality 128k "
    
    if cover_artwork:
        args += "--embed-thumbnail "

    os.system("youtube-dl" + " " + args + " " + link)


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
