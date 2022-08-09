from tkinter import *
from tkinter import ttk
from typing import List
from PIL import Image, ImageDraw, ImageTk
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import requests
from io import BytesIO
import sys
import os

sys.path.insert(0, os.path.join(os.getcwd(), "stagger"))
import stagger
from stagger.id3 import *

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

    def generate_thumbnail(self, image: Image.Image) -> Image.Image:

        orig_width = image.width
        orig_height = image.height
        # e.g. "1200 x 1200"
        res_label_string = str(orig_width) + " x " + str(orig_height)

        resized_image = image.resize((THUMBNAIL_SIZE, THUMBNAIL_SIZE))

        res_label_height = math.floor(THUMBNAIL_SIZE / 20)
        # Base width of res label on length of resolution text string
        res_label_width = math.floor(THUMBNAIL_SIZE / 30) * len(res_label_string) + 4

        strip = Image.new('RGB', (res_label_width, res_label_height)) #creating the black strip
        draw = ImageDraw.Draw(strip)
        
        # TODO: Right now, it's just using the default font.
        # If in the future, THUMBNAIL_SIZE actually has to get bigger, you might want to change the code below to something like this:
        # font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 16)
        # draw.text((0, 0), res_label_string, (255, 255, 255), font=font)

        draw.text((2, 0), res_label_string, (255, 255, 255)) #drawing text on the black strip
        offset = (0, THUMBNAIL_SIZE - res_label_height)
        resized_image.paste(strip, offset) #pasting black strip on the base image
        return resized_image

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
            image_pil = self.generate_thumbnail(self.images_pil[i])
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

# Returns tuple of (List[Image.Image], List[Bytes]) where both lists are the same length
# List of bytestrings are the directly downloaded image datas that will be used to create the pillow images
def search_cover_artwork_by_image(image: Image.Image):

    IMAGE_BUTTON_CLASS = "tdPRye"
    UPLOAD_IMAGE_TAB_CLASS = "iOGqzf H4qWMc aXIg1b"
    UPLOAD_IMAGE_TAB_XPATH =  "/html/body/div[1]/div[3]/div/div[2]/form/div[1]/div/a"
    BROWSE_BUTTON_ID = "awyMjb"
    ALL_SIZES_LINK_XPATH = "/html/body/div[7]/div/div[10]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/span[1]/a"
    ALL_IMAGE_THUMBNAILS_DIV_CLASS = "islrc"
    ALL_IMAGE_THUMBNAILS_DIV_XPATH = "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]"
    EXPANDED_IMAGE_XPATH = "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img"

    # Save given image as a file so we can upload it to google images
    image_path = os.path.join(os.getcwd(), "temp", "temp_image.jpg")
    image.save(image_path)

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
    browse_button.send_keys(image_path)
    

    # Click the "All sizes" link on the search results page to go to the list of image result thumbnails
    wait_for_section = WebDriverWait(driver, 180)
    wait_for_section.until(expected_conditions.presence_of_element_located((By.XPATH, ALL_SIZES_LINK_XPATH)))
    images_tab = driver.find_elements(By.XPATH, ALL_SIZES_LINK_XPATH)[0]
    images_tab.click()

    # We're done with the image file, delete it
    os.remove(image_path)

    # Get div that contains thumbnails of all the image results
    wait_for_section = WebDriverWait(driver, 180)
    wait_for_section.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, ALL_IMAGE_THUMBNAILS_DIV_CLASS)))
    thumbnails_div = driver.find_elements(By.CLASS_NAME, ALL_IMAGE_THUMBNAILS_DIV_CLASS)[0]
    
    # First element is just a thing that says "Image results", cut it out
    thumbnails = thumbnails_div.find_elements(By.XPATH, "./child::*")[1:] 

    # Find 5 highest resolution square thumbnails
    # TODO: Handle situation where there are fewer than 5 thumbnails (Foria - Tide)
    # Selector should be shrunk to be the right size for whatever number of images we do find
    top_five_resolutions = [0, 0, 0, 0, 0]
    top_five_thumbnails = [None, None, None, None, None]
    for thumbnail in thumbnails:
        width = int(thumbnail.get_attribute("data-ow"))
        height = int(thumbnail.get_attribute("data-oh"))
        
        # Skip images that aren't roughly square, they probably aren't cover artworks or are cropped weirdly
        if width < (float(height) * 0.95) or width > (float(height) * 1.05):
            continue
        
        # See if this image has better resolution than any we've already found
        for i, res in enumerate(top_five_resolutions):
            if width * height > res:
                # It does, add it to the list
                top_five_resolutions.insert(i, width * height)
                top_five_thumbnails.insert(i, thumbnail)

                # Trim off the worst item
                top_five_resolutions = top_five_resolutions[:-1]
                top_five_thumbnails = top_five_thumbnails[:-1]
                break
    
    full_size_images_pillow = []
    full_size_images_raw = []
    for thumbnail in top_five_thumbnails:
        thumbnail.click()

        # Get expanded image element from clicking thumbnail
        wait_for_section = WebDriverWait(driver, 180)
        wait_for_section.until(expected_conditions.presence_of_element_located((By.XPATH, EXPANDED_IMAGE_XPATH)))
        expanded_image = driver.find_elements(By.XPATH, EXPANDED_IMAGE_XPATH)[0]

        # Wait until full-sized image loads in (src changes from bas64 encoded thumbnail to a link that starts with http)
        # TODO: Handle situation where link is broken and full-res image never loads in (Shelter)
        # Cycle to next best image (which means that all images should be arranged in order of goodness beforehand)
        wait_for_full_res_image = WebDriverWait(driver, 180)
        wait_for_full_res_image.until(expected_conditions.text_to_be_present_in_element_attribute((By.XPATH, EXPANDED_IMAGE_XPATH), "src", "http"))
        
        image_url = expanded_image.get_attribute("src")

        response = requests.get(image_url)
        raw = response.content
        img = Image.open(BytesIO(raw))
        full_size_images_pillow.append(img)
        full_size_images_raw.append(raw)

    driver.close()

    # If the original image was a jpeg, we don't want to re-encode it when we're going from pillow to a file. 
    # Return both the pillow versions and the originals so that once user chooses an image, we can use the raw original image rather than the pillow version.
    return (full_size_images_pillow, full_size_images_raw)
        
def get_image_from_song_file(filename: str) -> Image.Image:
    tag = stagger.read_tag(filename)

    # Extract raw image bytes from metadata
    image_bytes = tag[APIC][0].data

    # Create pillow image
    image = Image.open(BytesIO(image_bytes))
    
    return image

def put_image_in_song_file(raw_image: bytes, filename: str):
    tag = stagger.read_tag(filename)
    
    image_path = filename + ".image"
    
    # Write image to a file becuase the stagger APIC constructor only takes a file path
    with open(image_path, "wb") as f:
        f.write(raw_image)

    tag[APIC] = APIC(image_path)    
    tag.write()

    os.remove(image_path)

if __name__ == "__main__":
    # # extracted_artwork = get_image_from_song_file("temp_artwork\\rick.mp3")
    # # searched_images_pillow, searched_images_raw = search_cover_artwork_by_image(extracted_artwork)

    searched_images_pillow = []
    for i in range(1, 6):
        searched_images_pillow.append(Image.open(f"D:\\soundscrape\\temp_artwork\\{i}.jpg"))

    selector = choose_image(searched_images_pillow)
    # # chosen_image_index = selector.show_selection_window()
    # # put_image_in_song_file(searched_images_raw[chosen_image_index], "temp_artwork\\rick.mp3")

    # generate_thumbnail(searched_images_pillow[0]).show()
    
    # and from here on, I save the image, create thumbnails, etc.