from unittest import TestCase
import os
from lyric_getter import extract_lyrics_from_html_genius, remove_newlines

def format_output_comparison(actual: str, expected: str):
    return f"\n----------------------\nExpected output:\n----------------------\n{expected}\n----------------------\nActual output:\n----------------------\n{actual}\n----------------------"

def remove_newlines_test(tester: TestCase, name):
    input_filename = os.path.join("test/remove_newlines_input", name + ".txt")
    expected_output_filename = os.path.join("test/remove_newlines_output", name + ".txt")

    with open(input_filename, "r", encoding="utf-8") as f:
        input_html = f.read()

    with open(expected_output_filename, "r", encoding="utf-8") as f:
        expected_output = f.read()

    actual_output = remove_newlines(input_html)
    
    format_output_comparison(actual_output, expected_output)
    tester.assertEqual(actual_output, expected_output)

def basic_test(tester: TestCase, name):
    input_html_filename = os.path.join("test/test_html_genius_basic", name + ".html")
    expected_output_filename = os.path.join("test/test_output_genius_basic", name + ".txt")

    with open(input_html_filename, "r", encoding="utf-8") as f:
        input_html = f.read()

    with open(expected_output_filename, "r", encoding="utf-8") as f:
        expected_output = f.read()

    actual_output = extract_lyrics_from_html_genius(input_html)
    
    format_output_comparison(actual_output, expected_output)
    tester.assertEqual(actual_output, expected_output)

class RemoveNewlineTests(TestCase):
    def test_remove_newlines_basic(self):
        remove_newlines_test(self, "remove_newlines_basic")   
    
    def test_remove_newlines_advanced(self):
        remove_newlines_test(self, "remove_newlines_basic")   

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

    def test_italic_parens(self):
        basic_test(self, "italic_parens")

    def test_square_brackets(self):
        basic_test(self, "italic_parens_inverted")

    def test_square_brackets(self):
        basic_test(self, "square_brackets")

    def test_square_brackets_italics(self):
        basic_test(self, "square_brackets_italics")

    def test_square_brackets_italics_newlines(self):
        basic_test(self, "square_brackets_italics_newlines")

    def test_annotation(self):
        basic_test(self, "annotation")

    def test_annotation_same_line(self):
        basic_test(self, "annotation_same_line")

    def test_annotation_break_outside_break(self):
        basic_test(self, "annotation_break_outside_break")

    def test_annotation_mid_breaks(self):
        basic_test(self, "annotation_mid_breaks")

    def test_annotation_mid_newlines(self):
        basic_test(self, "annotation_mid_newlines")

    def test_annotation_mid_mixed(self):
        basic_test(self, "annotation_mid_mixed")

    def test_span(self):
        basic_test(self, "span")
