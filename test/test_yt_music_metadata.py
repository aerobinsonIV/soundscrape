import os
import shutil
from unittest import TestCase
from youtube_downloader import get_yt_music_metadata

class YTMusicMetadataTests(TestCase):
    def test_mameyudoufu_i_dont_know_what_im_doing(self):
        link = "https://music.youtube.com/watch?v=meR1lgaP4ew"
        expected_metadata = "I don't know what I'm doing", "Mameyudoufu", "I don't know what I'm doing", "2021"
        dest_dir = os.path.join(os.getcwd(), "temp")
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        os.chdir("./temp")
        self.assertEqual(get_yt_music_metadata(link), expected_metadata)
        os.chdir("..")
        shutil.rmtree(dest_dir)

    def test_atmozfears_release(self):
        link = "https://music.youtube.com/watch?v=B-7m0EfW7LM"
        expected_metadata = "Release (feat. David Spekter)", "Atmozfears", "Release (feat. David Spekter)", None
        dest_dir = os.path.join(os.getcwd(), "temp")
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        os.chdir("./temp")
        self.assertEqual(get_yt_music_metadata(link), expected_metadata)
        os.chdir("..")
        shutil.rmtree(dest_dir)