import argparse
import os

def youtube_dl_wrapper(link: str, transcode_to_mp3: bool = False, cover_artwork: bool = False, music: bool = False):
    args = "--extract-audio"
    if transcode_to_mp3:
        args += "--audio-format mp3 --audio-quality 128k"
    
    if cover_artwork:
        args += "--embed-thumbnail"

    os.system("youtube-dl" + " " + args + " " + link)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--transcode-to-mp3", help="Transcode the downloaded opus file to mp3, lower quality but better compatibility", action='store_true')
    parser.add_argument("-c", "--cover-artwork", help="Embed video thumbnail as cover artwork", action='store_true')
    parser.add_argument("-m", "--music", help="Treat this as a YouTube music link (rather than e.g. a music video) and get the title, artist, and year from the webpage.", action='store_true')
    link_sources = parser.add_mutually_exclusive_group()
    link_sources.add_argument("-l", "--link-list", help="Pass in a text file containing a list of links for batch processing (one on each line).")
    link_sources.add_argument("-s", "--single-link", help="Pass a single URL to a YouTube song or video")
    
    args = parser.parse_args()

    if args.single_link != None:
        youtube_dl_wrapper(args.single_link, args.transcode_to_mp3, args.cover_artwork, args.music)
