from unittest import TestCase
import os
from lyric_adder import generate_lyrics_filename
from lyric_getter import search_term_preprocessing

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

