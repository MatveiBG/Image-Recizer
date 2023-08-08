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

def dirButton(txt, dir):
    dir.askChem()
    txt.set(dir)
    window.update()


base_dir = Direc()
final_dir = Direc()

window=Tk()
window.title('File transformer')
window.geometry("400x200+10+10")

window.bind('<ButtonRelease>', lambda x: checkButton(base_dir, final_dir))
window.grid_columnconfigure(1, weight=1)

btn=Button(
            window,
            text="Starting directory",
            fg='blue',
            command= lambda: dirButton(txtStart, base_dir)
            )

btn.grid(row = 1, column = 1, pady= 5)
txtStart = StringVar()
labelStart = Label(
    window,
    textvariable= txtStart
)

txtStart.set("Choose a starting directory.")
labelStart.grid(row= 2, column= 1, pady = 0)

btn2=Button(
            window,
            text="Final directory",
            fg='blue',
            command= lambda: dirButton(txtFin, final_dir)
            )
btn2.grid(row = 3, column = 1, pady= 5)
txtFin = StringVar()
labelFin = Label(
    window,
    textvariable= txtFin
)

txtFin.set("Choose a final directory.")
labelFin.grid(row= 4, column= 1, pady = 0)

btn3=Button(
            window,
            text="Transform",
            fg='blue',
            command= lambda: transformation(base_dir, final_dir, window),
            state= DISABLED         
            )
btn3.grid(row= 5, column = 1, pady= 5)

txtStatus = StringVar()
status = Label(
    window,
    textvariable= txtStatus
)

txtStatus.set("")
status.grid(row= 6, column= 1, pady = 0)
window.mainloop()
