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

def transform(base_dir, final_dir, removeBool, finBool):
        ''' Transforms a folder of images in required size,
        removes background if desired.
        base_dir: directory where files are taken from
        final_dir: directory where files are put after transformation
        removeBool: if True, images will go through background removal
        '''
        if finBool:
            os.mkdir(f'{base_dir}_new')
            final_dir = f'{base_dir}_new'
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

def checkButton(base_dir,final_dir, locked):
    ''' Called when one of the choosing buttons is pressed,
    if conditions are valiadated activates transform button,
    else keeps it off'''
    if locked: #if the final directory is auto-created
        if not base_dir.isEmpty():
            transButton.configure(state=NORMAL)
            window.update()
        else:
            transButton.configure(state=DISABLED)
            window.update()
    else:
        if yesDirectories(final_dir, base_dir):
            transButton.configure(state=NORMAL)
            window.update()
        else:
            transButton.configure(state=DISABLED)
            window.update()

def transformation(base_dir, final_dir, window, removeBool, finBool):
    ''' Called with the press of transform button,
    transforms images and updates status'''
    txtStatus.set("Processing images.")
    window.update()
    transform(base_dir, final_dir, removeBool, finBool)
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

window.bind('<ButtonRelease>', lambda x: checkButton(base_dir, final_dir, finDirVar.get()))
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
def finDirLock(lock):
    #locks button to choose final directory
    if lock:
        finButton.configure(state=DISABLED)
    else:
        finButton.configure(state=NORMAL)

finDirVar = BooleanVar()
checkCrtDir = Checkbutton(
    window,
    text = 'Create a final directory in same folder as original',
    variable= finDirVar,
    command = lambda: finDirLock(finDirVar.get())
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

#width entry
def delTextWidth(_):
    if widthEntry.get()=='Enter Desired Width':
        widthEntry.delete(0, 'end')
        widthEntry.configure(validatecommand = (vcmd, '%P'))
def checkTextWidth(_):
    if not widthEntry.get():
        widthEntry.configure(validatecommand = ())
        widthEntry.insert(0, 'Enter Desired Width')

widthEntry = Entry(sizeFrame, validate='all')

widthEntry.insert(0, 'Enter Desired Width')
widthEntry.grid(row= 0, column=0)

widthEntry.bind("<FocusIn>", delTextWidth)
widthEntry.bind("<FocusOut>", checkTextWidth)

#height entry
vcmd2 = window.register(checkDigit)
def delTextHeight(_):
    if heightEntry.get()=='Enter Desired Height':
        heightEntry.delete(0, 'end')
        heightEntry.configure(validatecommand = (vcmd2, '%P'))
def checkTextHeigth(_):
    if not heightEntry.get():
        heightEntry.configure(validatecommand = ())
        heightEntry.insert(0, 'Enter Desired Height')

heightEntry = Entry(sizeFrame, validate='all')

heightEntry.insert(0, 'Enter Desired Height')
heightEntry.grid(row= 1, column=0)

heightEntry.bind("<FocusIn>", delTextHeight)
heightEntry.bind("<FocusOut>", checkTextHeigth)

#size validation/change button
def lockEntry():
    widthEntry.configure(state= DISABLED)
    heightEntry.configure(state= DISABLED)

validateButton=Button(
            sizeFrame,
            text="Validate",
            fg='blue',
            command= lockEntry
            )
validateButton.grid(row = 0, column = 1)

def unlockEntry():
    widthEntry.configure(state= NORMAL)
    heightEntry.configure(state= NORMAL)

changeButton=Button(
            sizeFrame,
            text="Change",
            fg='blue',
            command= unlockEntry
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
            command= lambda: transformation(base_dir, final_dir, window, removeVar.get(), finDirVar.get()),
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
