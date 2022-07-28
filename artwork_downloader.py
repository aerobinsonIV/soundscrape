from email.mime import image
from typing import List
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


root = Tk()
frm = ttk.Frame(root, padding=60)
frm.grid()

with Image.open("D:\\soundscrape\\temp_artwork\\2.jpg") as im:
    image1_pil = im

image1_pil = image1_pil.resize((50, 50))

image1 = ImageTk.PhotoImage(image1_pil)
# Paste into ImageTk.PhotoImage
# https://pillow.readthedocs.io/en/stable/reference/ImageTk.html?highlight=imagetk
# image1.resize((50, 50))

ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", image=image1, command=root.destroy).grid(column=1, row=0)
root.mainloop()

# # List is a list of file paths to images
# def choose_image(images: List):
#     # Return filename of chosen image
#     return None