from unittest import TestCase
import os
from lyric_getter import extract_lyrics_from_html_genius

def basic_test(tester, name):
    input_html_filename = os.path.join("test/test_html_genius_basic", name + ".html")
    expected_output_filename = os.path.join("test/test_output_genius_basic", name + ".txt")

    with open(input_html_filename, "r", encoding="utf-8") as f:
        input_html = f.read()

    with open(expected_output_filename, "r", encoding="utf-8") as f:
        expected_output = f.read()

    actual_output = extract_lyrics_from_html_genius(input_html)

    tester.assertEqual(actual_output, expected_output)

class BasicTests(TestCase):
    def test_text(self):
        basic_test(self, "text")

    def test_start_newline(self):
        basic_test(self, "start_newline")
    
    def test_start_break(self):
        basic_test(self, "start_break")

    def test_mid_newline(self):
        basic_test(self, "mid_newline")
    
    def test_mid_break(self):
        basic_test(self, "mid_break")

    def test_end_newline(self):
        basic_test(self, "end_newline")
    
    def test_end_break(self):
        basic_test(self, "end_break")

    def test_many_mid_newlines(self):
        basic_test(self, "many_mid_newlines")
    
    def test_many_mid_breaks(self):
        basic_test(self, "many_mid_breaks")

    def test_parens(self):
        basic_test(self, "parens")

    def test_italics(self):
        basic_test(self, "italics")

    def test_italic_parens_(self):
        basic_test(self, "italic_parens")

    def test_italic_parens_inverted(self):
        basic_test(self, "italic_parens_inverted")
