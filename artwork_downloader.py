from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


root = Tk()

image_pil = Image.open(f"D:\\soundscrape\\temp_artwork\\2.jpg")
image_pil = image_pil.resize((1040, 600))

big_image = ImageTk.PhotoImage(image_pil)
ttk.Button(root, name="big", image=big_image, command=root.destroy).grid(column=0, row=0, columnspan=6)

images_tk = []
for i in range(1, 6):
    image_pil = Image.open(f"D:\\soundscrape\\temp_artwork\\{i}.jpg")
    image_pil = image_pil.resize((200, 200))

    images_tk.append(ImageTk.PhotoImage(image_pil))

    ttk.Button(root, name=str(i), image=images_tk[-1], command=root.destroy).grid(column=i, row=1)

def motion(event):
    x, y = event.x, event.y
    widget = event.widget

    try:
        image_index = int(widget._name)
        print(image_index)
    except:
        print(f"Not hovering an image {widget._name}")
        pass

    print(f'{x}, {y}')

root.bind('<Motion>', motion)
root.mainloop()

# # List is a list of file paths to images
# def choose_image(images: List):
#     # Return filename of chosen image
#     return None