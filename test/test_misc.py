from unittest import TestCase
from lyrics import clean_artist, clean_title, search_term_preprocessing, generate_lyrics_filename

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

