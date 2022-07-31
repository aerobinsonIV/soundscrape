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
ttk.Label(root, name="zoom_box", image=zoom_box_image_tk).grid(column=0, row=0, columnspan=NUM_THUMBNAILS + 1)
zoom_box_button = root.children["zoom_box"]

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
    if images_pil[i].width < zoom_box_width:
        width = images_pil[i].width
        size_multiplier = math.floor(zoom_box_width / width) + 1
        images_pil_resized.append(images_pil[i].resize((width * size_multiplier, width * size_multiplier), resample=Image.Resampling.NEAREST))
    else:
        images_pil_resized.append(images_pil[i])

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

    print(f'{x}, {y} on {image_index}')

    if image_index != -1:
        # TODO: Is there a way to do this mapping using pillow?
        original_image = images_pil_resized[image_index]
        original_image_size = original_image.width
        coord_multiplier = original_image_size / THUMBNAIL_SIZE

        mapped_x = x * coord_multiplier
        mapped_y = y * coord_multiplier

        left = mapped_x - math.floor(zoom_box_width / 2)
        top = mapped_y - math.floor(ZOOM_BOX_HEIGHT / 2)
        
        # TODO: use this as an excuse to learn those weird question mark oneliners because the goal is to become a snobby code elitist
        if left < 0:
            left = 0
        if top < 0:
            top = 0

        right = left + zoom_box_width
        bottom = top + ZOOM_BOX_HEIGHT

        box_tuple = (left, top, right, bottom)
        zoom_box_image = original_image.crop(box_tuple)
        zoom_box_image.show()
        zoom_box_image_tk = ImageTk.PhotoImage(zoom_box_image)
        zoom_box_button.configure(image=zoom_box_image_tk)

        print(f"Original image has size {original_image_size}, mapped coords are {mapped_x}, {mapped_y}")

root.bind('<Motion>', motion)
root.mainloop()

# # List is a list of file paths to images
# def choose_image(images: List):
#     # Return filename of chosen image
#     return None