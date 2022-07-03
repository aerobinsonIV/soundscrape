from unittest import TestCase
import os
from lyric_getter import extract_lyrics_from_html_genius

class DoubleLineBreaksGenius(TestCase):
    def test_predownloaded_html(self):
        html_dir = os.path.join(os.getcwd(), os.path.join("test", "test_html_genius"))
        html_files = os.listdir(html_dir)
        
        for html_file in html_files:
            full_path = os.path.join(html_dir, html_file)

            with open(full_path, "r", encoding="utf-8") as f:
                html = f.read()

            lyrics = extract_lyrics_from_html_genius(html)

            if "\n\n\n" in lyrics:
                raise Exception(f"Found double blank line in {html_file}")
