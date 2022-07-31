from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

THUMBNAIL_SIZE = 200

root = Tk()

image_pil = Image.open(f"D:\\soundscrape\\temp_artwork\\2.jpg")
image_pil = image_pil.resize((1040, 600))

big_image = ImageTk.PhotoImage(image_pil)
ttk.Button(root, name="big", image=big_image, command=root.destroy).grid(column=0, row=0, columnspan=6)

images_tk = []
for i in range(1, 6):
    image_pil = Image.open(f"D:\\soundscrape\\temp_artwork\\{i}.jpg")
    image_pil = image_pil.resize((THUMBNAIL_SIZE, THUMBNAIL_SIZE))

    images_tk.append(ImageTk.PhotoImage(image_pil))

    ttk.Button(root, name=str(i), image=images_tk[-1], command=root.destroy).grid(column=i, row=1)

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

root.bind('<Motion>', motion)
root.mainloop()

# # List is a list of file paths to images
# def choose_image(images: List):
#     # Return filename of chosen image
#     return None