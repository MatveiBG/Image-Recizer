import PIL.Image
import os
import tkinter
from tkinter import *
from tkinter import filedialog


class Direc():
    '''class used to define a directory path'''
    def __init__(self):
        self.chem = ""

    def askChem(self):
        self.chem = direc = filedialog.askdirectory(title='Select a directory')

    def __repr__(self):
        return self.chem
    
    def isEmpty(self):
        return self.chem == ""
    

exists = False


def transform(base_dir, final_dir, window, te):
    if base_dir.isEmpty() or final_dir.isEmpty():
        global exists
        if not exists:
            global label_exist
            label_exist = Label(window, text="Please choose a starting and final directory.")
            label_exist.pack()
            
            exists = True
    else:
        if exists:
            label_exist.destroy()
        basewidth = 912
        baseheight = 1100
        label = Label(window, text="Starting")
        label.pack()
        window.update()
        print("Starting")
        for images in os.listdir(str(base_dir)):
            bg = PIL.Image.new(mode="RGBA", size=(1200,1200), color="white")
            # check if the image ends with compatible extension
            if (images.endswith(".png") or images.endswith(".jpeg") or images.endswith(".jpg") or images.endswith(".webp")):
                try:
                    img = PIL.Image.open(f"{str(base_dir)}/{images}")
                    img = img.convert("RGBA")
                    wpercent = (basewidth/float(img.size[0]))
                    hsize = int((float(img.size[1])*float(wpercent)))
                    if int(hsize) < baseheight:
                        img = img.resize((basewidth,hsize), PIL.Image.Resampling.LANCZOS)
                    else:
                        wpercent = (baseheight/float(img.size[1]))
                        hsize = int((float(img.size[0])*float(wpercent)))
                        img = img.resize((hsize, baseheight), PIL.Image.Resampling.LANCZOS)
                    bg.paste(img, (int( 600 - img.size[0]/2 ), int( 600 - img.size[1]/2 ) ), img)
                    new_name = ""
                    for lettres in images:
                        if lettres != '.':
                            new_name += lettres
                        else:
                            break
                    bg.save(f'{str(final_dir)}/{new_name}_new.png') #final folder
                except TypeError:
                    print(f"Error with file {images}")

        print("Finished")
        label = Label(window, text="Finished")
        label.pack()

base_dir = Direc()
final_dir = Direc()


window=Tk()

te = Text(window, height = 5, width = 52)

btn=Button(window, text="Choose a starting directory", fg='blue', command= lambda: base_dir.askChem())
btn.place(x=80, y=60)

btn2=Button(window, text="Choose a final directory", fg='blue', command= lambda: final_dir.askChem())
btn2.place(x=80, y=100)

btn3=Button(window, text="Transform", fg='blue', command= lambda: transform(base_dir, final_dir, window, te))
btn3.place(x=80, y=140)
window.title('File transformer')
window.geometry("300x200+10+10")

window.mainloop()

