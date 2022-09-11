import os
import shutil
from unittest import TestCase
from PIL import Image
from artwork import search_cover_artwork_by_image, MAX_NUM_THUMBNAILS
from genius import get_artwork_image_genius, navigate_to_page_genius

TEST_ARTWORK_REL_PATH = "test\sandstorm.jpg"

def test_get_artwork(artist, title) -> int:
    image_dir = os.path.join(os.getcwd(), "images")

    if os.path.isdir(image_dir):
        shutil.rmtree(image_dir)
    
    os.mkdir(image_dir)

    image = get_artwork_image_genius(artist, title)
    image.close()
    
    images = os.listdir(image_dir)

    shutil.rmtree(image_dir)

    if len(images) == 1:
        return True
    else:
        return False

class TestGetGeniusArtwork(TestCase):
    def test_kid_laroi_erase_u(self):
        self.assertTrue(test_get_artwork("The Kid Laroi", "ERASE U"))

    # This one tests a bug that caused it to fail when LAROI was all caps
    def test_kid_laroi_selfish(self):
        self.assertTrue(test_get_artwork("The Kid LAROI", "SELFISH"))

    # The image for this song is stored on images.rapgenius.com instead of images.genius.com
    def test_nick_jonas_chains(self):
        self.assertTrue(test_get_artwork("Nick Jonas", "Chains"))

class TestGeniusNavigation(TestCase):
    def test_no_results(self):
        # Obviously this isn't a real song (at least at the time of writing)
        with self.assertRaises(Exception):
            navigate_to_page_genius("wefwfewefwwefwefwefwfwf", "eeeeeeeeeeeeeeeeeeeeee")

class TestReverseImageSearch(TestCase):
    def test_reverse_image_search(self):
        test_artwork_full_path = os.path.join(os.getcwd(), TEST_ARTWORK_REL_PATH)

        test_artwork = Image.open(test_artwork_full_path)

        found_images = search_cover_artwork_by_image(test_artwork)
        
        # Note that if enough good matches aren't found, fewer than MAX_NUM_THUMBNAILS images can be returned.
        # It's important that the test artwork be for a reasonably popular song so that we get plenty of results.
        self.assertEqual(len(found_images), MAX_NUM_THUMBNAILS)

