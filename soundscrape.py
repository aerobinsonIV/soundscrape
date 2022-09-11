import argparse
from genius import *
from lyrics import *
from artwork import *
from util import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--lyrics", help="Find and embed lyrics in song file(s)", action='store_true')
    parser.add_argument("-a", "--artwork", help="Find and embed cover artwork in song file(s)", action='store_true')
    parser.add_argument('path', nargs='?', default=os.path.join(os.getcwd(), "temp"))
    args = parser.parse_args()

    if not args.lyrics and not args.artwork:
        print("You have requested nothing. Your request has been fulfilled.")
        exit()

    if(len(sys.argv) < 2):
        print("Please specify a path.")
        exit()
        
    filenames = []

    song_file_path = args.path

    if os.path.isfile(song_file_path):
        # This is a single file
        filenames.append(song_file_path)
    elif os.path.isdir(song_file_path):
        dir_list = os.listdir(song_file_path)
        for file in dir_list:
            filenames.append(os.path.join(song_file_path, file))
    else:
        print("Invalid path.")
        exit()

    print("About to process the following files:")
    for filename in filenames:
        print(filename)

    for filename in filenames:
        scanned_title, scanned_artist = get_title_and_artist_from_filename(filename)
        cleaned_title = clean_title(scanned_title)
        cleaned_artist = clean_artist(scanned_artist)
        
        if args.lyrics:
            # If one song fails, just ignore it and keep going
            try:
                
                lyrics = get_lyrics_genius(cleaned_artist, cleaned_title)
                edited_lyrics = notepad(cleaned_artist, cleaned_title, lyrics)
                add_lyrics_to_song_file(filename, edited_lyrics)
            except:
                print(f"Failed to retrieve lyrics for {scanned_artist} - {scanned_title}.")

        if args.artwork:
            # Do cover artwork
            extracted_artwork = get_image_from_song_file(filename)
            searched_images_pillow, searched_images_raw = search_cover_artwork_by_image(extracted_artwork)
            selector = CoverArtSelector(searched_images_pillow)
            chosen_image_index = selector.show_selection_window()
            put_image_in_song_file(searched_images_raw[chosen_image_index], filename)