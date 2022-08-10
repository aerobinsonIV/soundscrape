from ast import parse
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--transcode-to-mp3", help="Transcode the downloaded opus file to mp3, lower quality but better compatibility", action='store_true')
    parser.add_argument("-c", "--cover-artwork", help="Embed video thumbnail as cover artwork", action='store_true')
    parser.add_argument("-m", "--music", help="Treat this as a YouTube music link (rather than e.g. a music video) and get the title, artist, and year from the webpage.", action='store_true')
    link_sources = parser.add_mutually_exclusive_group()
    link_sources.add_argument("-l", "--link-list", help="Pass in a text file containing a list of links for batch processing (one on each line).")
    link_sources.add_argument("-s", "--single-link", help="Pass a single URL to a YouTube song or video")
    
    args = parser.parse_args()
    print(args.link_list)
    print(args.music)