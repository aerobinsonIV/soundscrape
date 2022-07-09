from unittest import TestCase
import os
from lyric_getter import search_term_preprocessing

class MiscTests(TestCase):
    def test_predownloaded_html(self):
        input = "cool & good"
        expected_output = "cool %26 good"

        self.assertEqual(search_term_preprocessing(input), expected_output)
