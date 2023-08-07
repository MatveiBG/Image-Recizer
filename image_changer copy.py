import PIL.Image
import os
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter  import ttk


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
    
def noDirectories(dir1: Direc, dir2: Direc):
    ''' Returns true if both directories have not been filled yet'''
    if dir1.isEmpty() and dir2.isEmpty():
        return True

def yesDirectories(dir1: Direc, dir2: Direc):
    ''' Returns true if both directories have not been filled yet'''
    if not dir1.isEmpty() and not dir2.isEmpty():
        return True

def transform(base_dir, final_dir):
        basewidth = 912
        baseheight = 1100
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

def checkButton(base_dir,final_dir):
    if yesDirectories(final_dir, base_dir):
        btn3.configure(state=NORMAL)
        window.update()

def transformation(base_dir, final_dir, window):
    txtStatus.set("Processing images.")
    window.update()
    transform(base_dir, final_dir)
    txtStatus.set("Finished.")
    window.update()


base_dir = Direc()
final_dir = Direc()

window=Tk()
window.title('File transformer')
window.geometry("300x200+10+10")

window.bind('<ButtonRelease>', lambda x: checkButton(base_dir, final_dir))
window.grid_columnconfigure(1, weight=1)
te = Text(window, height = 5, width = 52)

btn=Button(
            window,
            text="Starting directory",
            fg='blue',
            command= lambda: base_dir.askChem()
            )

btn.grid(row = 1, column = 1, pady= 10)

btn2=Button(
            window,
            text="Final directory",
            fg='blue',
            command= lambda: final_dir.askChem()
            )
btn2.grid(row = 2, column = 1, pady= 10)

btn3=Button(
            window,
            text="Transform",
            fg='blue',
            command= lambda: transformation(base_dir, final_dir, window),
            state= DISABLED         
            )
btn3.grid(row= 3, column = 1, pady= 10)

txtStatus = StringVar()
status = Label(
    window,
    textvariable= txtStatus
)

txtStatus.set("Choose starting and final directory.")
status.grid(row= 4, column= 1, pady = 5)
window.mainloop()
