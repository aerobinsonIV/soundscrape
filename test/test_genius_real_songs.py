from unittest import TestCase
import os
from lyrics import extract_lyrics_from_html_genius

def write_actual_output_file(filename, actual_output):
    # Does cache dir exist?

    actual_output_dir = "test/actual_output_genius"

    # Create the actual output dir if it doesn't already exist
    if not os.path.isdir("test/actual_output_genius"):
        os.mkdir("test/actual_output_genius")
        
    with open(os.path.join(actual_output_dir, filename + ".txt"), "w", encoding="utf-8") as f:
        f.write(actual_output)

def real_song_test(tester: TestCase, name):
    input_html_filename = os.path.join("test/test_html_genius", name + ".html")
    expected_output_filename = os.path.join("test/test_output_genius", name + ".txt")

    with open(input_html_filename, "r", encoding="utf-8") as f:
        input_html = f.read()

    with open(expected_output_filename, "r", encoding="utf-8") as f:
        expected_output = f.read()

    actual_output = extract_lyrics_from_html_genius(input_html)
    write_actual_output_file(name, actual_output)
    tester.assertEqual(actual_output, expected_output)

class RealSongTests(TestCase):
    def test_chase_atlantic_beauty_in_death(self):
        real_song_test(self, "beauty_in_death")

    def test_chase_atlantic_cassie(self):
        real_song_test(self, "cassie")

    def test_chase_atlantic_call_me_back(self):
        real_song_test(self, "call_me_back")

    def test_lil_nas_x_old_town_road(self):
        real_song_test(self, "lil_nas_x_old_town_road")

    def test_cloudfield_artificial(self):
        real_song_test(self, "cloudfield_artificial")

    def test_chase_atlantic_escort(self):
        real_song_test(self, "chase_atlantic_escort")

    def test_chase_atlantic_i_never_existed(self):
        real_song_test(self, "chase_atlantic_i_never_existed")

    def test_chase_atlantic_obsessive(self):
        real_song_test(self, "chase_atlantic_obsessive")

    def test_essenger_lexi_norton_downfall(self):
        real_song_test(self, "essenger_lexi_norton_downfall")