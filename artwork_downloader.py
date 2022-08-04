from tkinter import *
from tkinter import ttk
from typing import List
from PIL import Image, ImageTk
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

THUMBNAIL_SIZE = 200
ZOOM_BOX_HEIGHT = 600

class CoverArtSelector():
    def motion(self, event):
        # Buttons have 5px padding, subtract to get exact coords relative to image
        x, y = event.x - 5, event.y - 5
        widget = event.widget

        try:
            self.image_index = int(widget._name)
        except:
            # We're not on an image
            self.image_index = -1
            pass

        if self.image_index != -1:

            # Even if the mouse is on a button, it may still be outside the image. 
            # If it's in the small padding area on the edge, we don't consider it to be on an image.
            if x < 0 or y < 0:
                self.image_index = -1

            if x > THUMBNAIL_SIZE or y > THUMBNAIL_SIZE:
                self.image_index = -1

        if self.image_index != -1:
            # TODO: Is there a way to do this mapping using pillow?
            original_image = self.images_pil_resized[self.image_index]
            original_image_size = original_image.width
            coord_multiplier = original_image_size / THUMBNAIL_SIZE

            mapped_x = x * coord_multiplier
            mapped_y = y * coord_multiplier

            # TODO: use this as an excuse to learn those weird question mark oneliners because the goal is to become a snobby code elitist
            if mapped_x > self.zoom_box_width / 2:
                # Calc x based on right edge
                right = mapped_x + math.ceil(self.zoom_box_width / 2)
                if right > original_image_size:
                    right = original_image_size
                left = right - self.zoom_box_width
            else:
                # Calc x based on left edge
                left = mapped_x - math.floor(self.zoom_box_width / 2)
                if left < 0:
                    left = 0
                right = left + self.zoom_box_width

            if mapped_y > self.zoom_box_width / 2:
                # Calc y based on bottom edge
                bottom = mapped_y + math.ceil(ZOOM_BOX_HEIGHT / 2)
                if bottom > original_image_size:
                    bottom = original_image_size
                top = bottom - ZOOM_BOX_HEIGHT
            else:
                # Calc y based on top edge
                top = mapped_y - math.floor(ZOOM_BOX_HEIGHT / 2)
                if top < 0:
                    top = 0
                bottom = top + ZOOM_BOX_HEIGHT

            box_tuple = (left, top, right, bottom)
            zoom_box_image = original_image.crop(box_tuple)
            
            zoom_box_image_tk = ImageTk.PhotoImage(zoom_box_image)
            self.zoom_box_label.configure(image=zoom_box_image_tk)

            self.anti_garbage_collection_list[0] = zoom_box_image_tk

    def __init__(self, images: List) -> None:
        # Load all thumnbail images
        # TODO: Ensure these are all square, do centered cropping if they aren't
        self.images_pil = []
        for image in images:
            self.images_pil.append(image)

    def show_selection_window(self) -> int:  
        num_thumbnails = len(self.images_pil)

        self.root = Tk()

        self.zoom_box_width = num_thumbnails * THUMBNAIL_SIZE + (num_thumbnails - 1) * 10 # Calculate zoom area width
        image_pil = Image.new(mode="RGB", size =(self.zoom_box_width, ZOOM_BOX_HEIGHT)) # Create placeholder image for zoom area
        zoom_box_image_tk = ImageTk.PhotoImage(image_pil) # Make placeholder image into ImageTK

        # Hack to prevent the zoomed image from getting garbage collected by TCL
        # See https://stackoverflow.com/a/71502573
        self.anti_garbage_collection_list = []
        self.anti_garbage_collection_list.append(zoom_box_image_tk)

        ttk.Label(self.root, name="zoom_box", image=zoom_box_image_tk).grid(column=0, row=0, columnspan=num_thumbnails + 1)
        self.zoom_box_label = self.root.children["zoom_box"]

        # Create thumbnail buttons
        self.images_tk = []
        for i in range(len(self.images_pil)):
            image_pil = self.images_pil[i].resize((THUMBNAIL_SIZE, THUMBNAIL_SIZE))
            self.images_tk.append(ImageTk.PhotoImage(image_pil))
            ttk.Button(self.root, name=str(i), image=self.images_tk[-1], command=self.root.destroy).grid(column=i, row=1)

        # If any of the original images are smaller than the width of the zoomed area, scale them up
        self.images_pil_resized = []
        for i in range(num_thumbnails): 
            width = self.images_pil[i].width
            if width < self.zoom_box_width:
                size_multiplier = math.floor(self.zoom_box_width / width) + 1
            else:
                # Double zoom of even high-res images just so we can get a better look at the details
                size_multiplier = 2
            
            self.images_pil_resized.append(self.images_pil[i].resize((width * size_multiplier, width * size_multiplier), resample=Image.Resampling.NEAREST))

        self.root.bind('<Motion>', self.motion)
        self.root.mainloop()
        return self.image_index

# List is a list of pillow images
def choose_image(images: List):
    selector = CoverArtSelector(images)
    return selector.show_selection_window()

def search_cover_artwork_by_image(image):

    IMAGE_BUTTON_CLASS = "tdPRye"
    UPLOAD_IMAGE_TAB_CLASS = "iOGqzf H4qWMc aXIg1b"
    UPLOAD_IMAGE_TAB_XPATH =  "/html/body/div[1]/div[3]/div/div[2]/form/div[1]/div/a"
    BROWSE_BUTTON_ID = "awyMjb"
    ALL_SIZES_LINK_XPATH = "/html/body/div[7]/div/div[10]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/span[1]/a"
    ALL_IMAGE_THUMBNAILS_DIV_CLASS = "islrc"
    ALL_IMAGE_THUMBNAILS_DIV_XPATH = "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]"

    driver = webdriver.Firefox()
    
    ublock_origin_path = "ublock_origin-1.43.0.xpi"
    driver.install_addon(ublock_origin_path)

    driver.get(f'https://images.google.com')
    
    # Click the image button with the camera icon
    wait_for_section = WebDriverWait(driver, 180)
    wait_for_section.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, IMAGE_BUTTON_CLASS)))
    image_button = driver.find_elements(By.CLASS_NAME, IMAGE_BUTTON_CLASS)[0]
    image_button.click()

    # Click the "Upload an image" tab
    wait_for_section = WebDriverWait(driver, 180)
    wait_for_section.until(expected_conditions.presence_of_element_located((By.XPATH, UPLOAD_IMAGE_TAB_XPATH)))
    upload_image_tab = driver.find_elements(By.XPATH, UPLOAD_IMAGE_TAB_XPATH)[0]
    upload_image_tab.click()

    # Click the "Browse" button to upload the image
    wait_for_section = WebDriverWait(driver, 180)
    wait_for_section.until(expected_conditions.presence_of_element_located((By.ID, BROWSE_BUTTON_ID)))
    browse_button = driver.find_elements(By.ID, BROWSE_BUTTON_ID)[0]
    browse_button.send_keys('D:\soundscrape\\temp_artwork\\1.jpg')

    # Click the "All sizes" link on the search results page to go to the list of image result thumbnails
    wait_for_section = WebDriverWait(driver, 180)
    wait_for_section.until(expected_conditions.presence_of_element_located((By.XPATH, ALL_SIZES_LINK_XPATH)))
    images_tab = driver.find_elements(By.XPATH, ALL_SIZES_LINK_XPATH)[0]
    images_tab.click()

    # Get div that contains thumbnails of all the image results
    wait_for_section = WebDriverWait(driver, 180)
    wait_for_section.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, ALL_IMAGE_THUMBNAILS_DIV_CLASS)))
    thumbnails_div = driver.find_elements(By.CLASS_NAME, ALL_IMAGE_THUMBNAILS_DIV_CLASS)[0]
    
    # First element is just a thing that says "Image results", cut it out
    thumbnails = thumbnails_div.find_elements_by_xpath("./child::*")[1:] 

    image_dimensions = []
    for thumbnail in thumbnails:
        width = thumbnail.get_attribute("data-ow")
        height = thumbnail.get_attribute("data-oh")
        image_dimensions.append((width, height))

    for pair in image_dimensions:
        print(pair)

    # TODO: Find top 5 square images with the highest resolutions, download all 5 by clicking their thumbnails and downloading the original image, get all 5 into cover art UI
        
if __name__ == "__main__":
    artwork_images = []
    for i in range(1, 6):
        artwork_images.append(Image.open(f"D:\\soundscrape\\temp_artwork\\{i}.jpg"))

    search_cover_artwork_by_image(artwork_images[0])
    