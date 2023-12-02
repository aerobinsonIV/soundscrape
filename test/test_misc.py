import os
import sys
import shutil
from unittest import TestCase
from lyrics import add_lyrics_to_song_file, clean_artist, clean_title, search_term_preprocessing, generate_lyrics_filename

sys.path.insert(0, os.path.join(os.getcwd(), "stagger"))
import stagger
from stagger.id3 import *

class MiscTests(TestCase):
    def test_predownloaded_html(self):
        input = "cool & good"
        expected_output = "cool %26 good"

        self.assertEqual(search_term_preprocessing(input), expected_output)
    
    def test_generate_lyrics_filename(self):
        input_artist = "\\\\The Backslashes\\\\   "
        input_title = "   OwO, what's this?"
        expected_output = "the_backslashes_owo,_what's_this.txt"

        self.assertEqual(generate_lyrics_filename(input_artist, input_title), expected_output)

    def test_clean_title_parens(self):
        input_title = "Downfall (feat. Lexi Norton)"
        expected_output = "Downfall"

        self.assertEqual(clean_title(input_title), expected_output)

    def test_clean_title_ft(self):
        input_title = "Clarity ft. Foxes"
        expected_output = "Clarity"

        self.assertEqual(clean_title(input_title), expected_output)

    def test_clean_title_feat(self):
        input_title = "Emotional feat. Matthew Koma"
        expected_output = "Emotional"

        self.assertEqual(clean_title(input_title), expected_output)

    def test_clean_title_mixed(self):
        input_title = "Talk About It Feat. Desirée Dawson [Virtual Riot Remix]"
        expected_output = "Talk About It"

        self.assertEqual(clean_title(input_title), expected_output)

    def test_clean_artist(self):
        input_artist = "Virual Riot; Submatik, Holly Drummond"
        expected_output = "Virual Riot Submatik Holly Drummond"

        self.assertEqual(clean_artist(input_artist), expected_output)

    # This test doesn't properly isolate the issue
    def test_lyrics_properly_terminated(self):
        dest_dir = os.path.join(os.getcwd(), "temp")
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        src = os.path.join(os.getcwd(), "test/yeet.mp3")
        dest = os.path.join(os.getcwd(), "temp/yeet.mp3")
        shutil.copyfile(src, dest)

        lyrics = "yeet"

        add_lyrics_to_song_file(dest, lyrics)

        tag = stagger.read_tag(dest)
        tag_lyrics = tag['USLT'].text[0][4:]
        self.assertEqual(tag_lyrics, lyrics)
        os.remove(dest)
        shutil.rmtree(dest_dir)

