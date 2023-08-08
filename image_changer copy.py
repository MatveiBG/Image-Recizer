import PIL.Image
import os
import tkinter
from tkinter import *
from tkinter import filedialog
from rembg import remove

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

def transform(base_dir, final_dir, removeBool):
        ''' Transforms a folder of images in required size,
        removes background if desired.
        base_dir: directory where files are taken from
        final_dir: directory where files are put after transformation
        removeBool: if True, images will go through background removal
        '''
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
                    if removeBool:
                        img = remove(img)
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
    ''' Called when one of the choosing buttons is pressed,
    if conditions are valiadated activates transform button,
    else keeps it off'''
    if yesDirectories(final_dir, base_dir):
        transButton.configure(state=NORMAL)
        window.update()
    else:
        transButton.configure(state=DISABLED)
        window.update()

def transformation(base_dir, final_dir, window, removeBool):
    ''' Called with the press of transform button,
    transforms images and updates status'''
    txtStatus.set("Processing images.")
    window.update()
    transform(base_dir, final_dir, removeBool)
    txtStatus.set("Finished.")
    window.update()

def dirButton(txt, dir, strt):
    ''' Called with the press of directory buttons,
    used to get user choice of directory and show selected direcotry after'''
    dir.askChem()
    if dir.isEmpty(): #if no directory has been choosen displays instructions
        txt.set("Choose a starting directory." if strt else  "Choose a final directory.")
    else:
        txt.set(dir)
    window.update()

#Instacing paths#
base_dir = Direc()
final_dir = Direc()
#################

#Window setup####
window=Tk()
window.title('File transformer')
window.geometry("500x275+10+10")

window.bind('<ButtonRelease>', lambda x: checkButton(base_dir, final_dir))
window.grid_columnconfigure(1, weight=1)
#################

#checkbox for bg removal
removeVar = BooleanVar()
checkRmv = Checkbutton(
    window,
    text = 'Remove background of images',
    variable= removeVar,
    command = lambda: print(removeVar.get())
)
checkRmv.grid(row=0, column=1)

#checkbox for final directory creation
finDirVar = BooleanVar()
checkCrtDir = Checkbutton(
    window,
    text = 'Create a final directory in same folder as original',
    variable= removeVar,
    command = lambda: print(removeVar.get())
)
checkCrtDir.grid(row= 1, column= 1)

#size frame
sizeFrame = Frame(window)
sizeFrame.grid(row= 2, column=1)

#size entry
def checkDigit(P):
    if str.isdigit(P) or P == '':
        return True
    else:
        return False
vcmd = window.register(checkDigit)
widthEntry = Entry(sizeFrame, validate='all', validatecommand=(vcmd, '%P'))
widthEntry.grid(row= 0, column=0)
heightEntry = Entry(sizeFrame, validate='all', validatecommand=(vcmd, '%P'))
heightEntry.grid(row= 1, column=0)

#size validation/change button
validateButton=Button(
            sizeFrame,
            text="Validate",
            fg='blue',
            command= lambda: dirButton(txtFin, final_dir, False)
            )
validateButton.grid(row = 0, column = 1)

changeButton=Button(
            sizeFrame,
            text="Change",
            fg='blue',
            command= lambda: dirButton(txtFin, final_dir, False)
            )
changeButton.grid(row = 1, column = 1)

#directory buttons frame
dirFrame = Frame(window)
dirFrame.grid(row= 3, column= 1)

#button for initial directory
startButton=Button(
            dirFrame,
            text="Starting directory",
            fg='blue',
            command= lambda: dirButton(txtStart, base_dir, True)
            )
startButton.grid(row = 0, column = 0, pady= 0)

#label for initial directory choice
txtStart = StringVar()
labelStart = Label(
    dirFrame,
    textvariable= txtStart
)

txtStart.set("Choose a starting directory.")
labelStart.grid(row= 1, column= 0, pady = 0)

#button for final directory
finButton=Button(
            dirFrame,
            text="Final directory",
            fg='blue',
            command= lambda: dirButton(txtFin, final_dir, False)
            )
finButton.grid(row = 2, column = 0, pady= 0)

#label for final directory choice
txtFin = StringVar()
labelFin = Label(
    dirFrame,
    textvariable= txtFin
)
txtFin.set("Choose a final directory.")
labelFin.grid(row= 3, column= 0, pady = 0)

#button to do transformation
transButton=Button(
            window,
            text="Transform",
            fg='blue',
            command= lambda: transformation(base_dir, final_dir, window, removeVar.get()),
            state= DISABLED         
            )
transButton.grid(row= 4, column = 1, pady= 0)

#label for transformation status and instructions
txtStatus = StringVar()
status = Label(
    window,
    textvariable= txtStatus
)
txtStatus.set("")
status.grid(row= 5, column= 1, pady = 0)

window.mainloop()
