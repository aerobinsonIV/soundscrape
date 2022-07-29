from email.mime import image
from typing import List
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


root = Tk()
frm = ttk.Frame(root, padding=60)
frm.grid()

images_tk = []
for i in range(1, 6):
    image_pil = Image.open(f"D:\\soundscrape\\temp_artwork\\{i}.jpg")
    image_pil = image_pil.resize((200, 200))

    images_tk.append(ImageTk.PhotoImage(image_pil))

    ttk.Button(frm, image=images_tk[-1], command=root.destroy).grid(column=i, row=0)

def motion(event):
    x, y = event.x, event.y
    print(f'{x}, {y}')

root.bind('<Motion>', motion)
root.mainloop()

# # List is a list of file paths to images
# def choose_image(images: List):
#     # Return filename of chosen image
#     return None