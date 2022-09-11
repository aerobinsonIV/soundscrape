import os
import shutil
from unittest import TestCase
from genius import get_artwork_image_genius

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

        

