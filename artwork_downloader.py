from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import math
from time import sleep

THUMBNAIL_SIZE = 200
NUM_THUMBNAILS = 5
ZOOM_BOX_HEIGHT = 600

root = Tk()

image_pil = Image.open(f"D:\\soundscrape\\temp_artwork\\2.jpg")

zoom_box_width = NUM_THUMBNAILS * THUMBNAIL_SIZE + (NUM_THUMBNAILS - 1) * 10
image_pil = image_pil.resize((zoom_box_width, ZOOM_BOX_HEIGHT))

zoom_box_image_tk = ImageTk.PhotoImage(image_pil)

# Hack to prevent the zoomed image from getting garbage collected by TCL
# See https://stackoverflow.com/a/71502573
anti_garbage_collection_list = []
anti_garbage_collection_list.append(zoom_box_image_tk)

ttk.Label(root, name="zoom_box", image=zoom_box_image_tk).grid(column=0, row=0, columnspan=NUM_THUMBNAILS + 1)
zoom_box_label = root.children["zoom_box"]

# Load all thumnbail images
# TODO: Ensure these are all square, do centered cropping if they aren't
images_pil = []
for i in range(1, NUM_THUMBNAILS + 1):
    images_pil.append(Image.open(f"D:\\soundscrape\\temp_artwork\\{i}.jpg"))

# Resize images to thumbnail size, convert to tk, make into button
images_tk = []
for i in range(NUM_THUMBNAILS):
    image_pil = images_pil[i].resize((THUMBNAIL_SIZE, THUMBNAIL_SIZE))
    images_tk.append(ImageTk.PhotoImage(image_pil))
    ttk.Button(root, name=str(i), image=images_tk[-1], command=root.destroy).grid(column=i, row=1)

# If any of the original images are smaller than the width of the zoomed area, scale them up
images_pil_resized = []
for i in range(NUM_THUMBNAILS): 
    width = images_pil[i].width
    if width < zoom_box_width:
        size_multiplier = math.floor(zoom_box_width / width) + 1
    else:
        # Double zoom of even high-res images just so we can get a better look at the details
        size_multiplier = 2
    
    images_pil_resized.append(images_pil[i].resize((width * size_multiplier, width * size_multiplier), resample=Image.Resampling.NEAREST))

def motion(event):
    # Buttons have 5px padding, subtract to get exact coords relative to image
    x, y = event.x - 5, event.y - 5
    widget = event.widget

    try:
        image_index = int(widget._name)
    except:
        # We're not on an image
        image_index = -1
        pass

    if image_index != -1:

        # Even if the mouse is on a button, it may still be outside the image. 
        # If it's in the small padding area on the edge, we don't consider it to be on an image.
        if x < 0 or y < 0:
            image_index = -1

        if x > THUMBNAIL_SIZE or y > THUMBNAIL_SIZE:
            image_index = -1

    if image_index != -1:
        # TODO: Is there a way to do this mapping using pillow?
        original_image = images_pil_resized[image_index]
        original_image_size = original_image.width
        coord_multiplier = original_image_size / THUMBNAIL_SIZE

        mapped_x = x * coord_multiplier
        mapped_y = y * coord_multiplier

        # TODO: use this as an excuse to learn those weird question mark oneliners because the goal is to become a snobby code elitist
        if mapped_x > zoom_box_width / 2:
            # Calc x based on right edge
            right = mapped_x + math.ceil(zoom_box_width / 2)
            if right > original_image_size:
                right = original_image_size
            left = right - zoom_box_width
        else:
            # Calc x based on left edge
            left = mapped_x - math.floor(zoom_box_width / 2)
            if left < 0:
                left = 0
            right = left + zoom_box_width

        if mapped_y > zoom_box_width / 2:
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
        zoom_box_label.configure(image=zoom_box_image_tk)

        anti_garbage_collection_list[0] = zoom_box_image_tk

root.bind('<Motion>', motion)
root.mainloop()

# # List is a list of file paths to images
# def choose_image(images: List):
#     # Return filename of chosen image
#     return None