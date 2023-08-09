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

def transform(base_dir, final_dir, removeBool, finBool, size, back, color):
        ''' Transforms a folder of images in required size,
        removes background if desired.
        base_dir: directory where files are taken from
        final_dir: directory where files are put after transformation
        removeBool: if True, images will go through background removal
        '''
        if finBool:
            finStr = f'{base_dir}_new/'
            print(finStr)
            if os.path.exists(finStr):
                counter = 1
                finStr = finStr[:-1] + f'_({counter})/'
                while os.path.exists(finStr):
                    counter += 1
                    finStr = finStr[:-3] + f'{counter})/'
            os.mkdir(finStr)
            final_dir = finStr
        basewidth = size[0]
        baseheight = size[1]
        print(basewidth, baseheight)
        print("Starting")
        for images in os.listdir(str(base_dir)):
            bg = PIL.Image.new(mode="RGBA", size=(back,back), color=None if color =='Transparent' else color)
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
                    bg.paste(img, (int( back/2 - img.size[0]/2 ), int( back/2 - img.size[1]/2 ) ), img)
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
    if widthEntry["state"] == DISABLED:
        if locked: #if the final directory is auto-created
            if not base_dir.isEmpty():
                transButton.configure(state=NORMAL)
            else:
                transButton.configure(state=DISABLED)
        else:
            if yesDirectories(final_dir, base_dir):
                transButton.configure(state=NORMAL)
            else:
                transButton.configure(state=DISABLED)
                
    else:
        transButton.configure(state=DISABLED)
        
    if locked:
        txtFin.set('Final directory will be created.')
    else:
        txtFin.set('Choose a final directory.')

    window.update()

def transformation(base_dir, final_dir, window, removeBool, finBool, size, bg, color):
    ''' Called with the press of transform button,
    transforms images and updates status'''
    newSize = []
    if size[0].isdigit():
        newSize.append(int(size[0]))
    else:
        newSize.append(912)
    if size[1].isdigit():
        newSize.append(int(size[1]))
    else:
        newSize.append(1100)
    if bg.isdigit():
       bg = int(bg)
    else:
        bg = 1200 
    txtStatus.set("Processing images.")
    window.update()
    transform(base_dir, final_dir, removeBool, finBool, newSize, bg, color)
    txtStatus.set("Finished.")
    window.update()

def dirButton(txt, dir, strt):
    ''' Called with the press of directory buttons,
    used to get user choice of directory and show selected directory after'''
    dir.askChem()
    if dir.isEmpty(): #if no directory has been choosen displays instructions
        txt.set("Choose a starting directory." if strt else  "Choose a final directory.")
    else:
        txt.set(dir)
    window.update()
    statusUpdate()

#Instacing paths#
base_dir = Direc()
final_dir = Direc()
#################

#Window setup####
window=Tk()
window.title('File transformer')
window.geometry("500x325+10+10")

window.bind('<ButtonRelease>', lambda x: checkButton(base_dir, final_dir, finDirVar.get()))
window.grid_columnconfigure(1, weight=1)
#################

'''
#initial popup
popup = Toplevel()
label = Label(popup, text="Welcome to the image transformer,\n"
              "Choose a directory (folder) where you want your images taken from\n"
              "and either choose a destination for your transformed images\n"
              "or choose the option to create a new folder for them.\n"
              "If the images have a background that you want to remove check 'remove background' box.")
label.pack(fill='x', padx=50, pady=5)
button_close = Button(popup, text="Close", command=popup.destroy)
button_close.pack(fill='x')
'''

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
    statusUpdate()

finDirVar = BooleanVar()
checkCrtDir = Checkbutton(
    window,
    text = 'Create a final directory in same folder as original',
    variable= finDirVar,
    command = lambda: finDirLock(finDirVar.get())
    )
checkCrtDir.grid(row= 1, column= 1)

#color frame
colorFrame = Frame()
colorFrame.grid(row= 2, column= 1)

#color label
txtColor = StringVar()
labelColor = Label(
    colorFrame,
    textvariable= txtColor
)
txtColor.set("Background color:")
labelColor.grid(row= 0, column= 0, pady = 0)

#color dropdown
clicked = StringVar()
clicked.set('White')
colorOptions = [
    'White',
    'Black',
    'Red',
    'Green',
    'Blue',
    'Cyan',
    'Yellow',
    'Magenta',
    'Transparent',
]
colors = OptionMenu(colorFrame, clicked, *colorOptions)
colors.grid(row = 0, column = 1)


#size frame
sizeFrame = Frame(window)
sizeFrame.grid(row= 3, column=1)

#size entry
def checkDigit(P):
    if str.isdigit(P) or P == '':
        return True
    else:
        return False
vcmd = window.register(checkDigit)

#width entry
def delTextWidth(_):
    if widthEntry.get()=='Enter Width (912)':
        widthEntry.delete(0, 'end')
        widthEntry.configure(validatecommand = (vcmd, '%P'))
def checkTextWidth(_):
    if not widthEntry.get():
        widthEntry.configure(validatecommand = ())
        widthEntry.insert(0, 'Enter Width (912)')

widthEntry = Entry(sizeFrame, validate='all')

widthEntry.insert(0, 'Enter Width (912)')
widthEntry.grid(row= 0, column=0)

widthEntry.bind("<FocusIn>", delTextWidth)
widthEntry.bind("<FocusOut>", checkTextWidth)

#height entry
vcmd2 = window.register(checkDigit)
def delTextHeight(_):
    if heightEntry.get()=='Enter Height (1100)':
        heightEntry.delete(0, 'end')
        heightEntry.configure(validatecommand = (vcmd2, '%P'))
def checkTextHeigth(_):
    if not heightEntry.get():
        heightEntry.configure(validatecommand = ())
        heightEntry.insert(0, 'Enter Height (1100)')

heightEntry = Entry(sizeFrame, validate='all')

heightEntry.insert(0, 'Enter Height (1100)')
heightEntry.grid(row= 1, column=0)

heightEntry.bind("<FocusIn>", delTextHeight)
heightEntry.bind("<FocusOut>", checkTextHeigth)

#bg size entry
def delTextSize(_):
    if sizeEntry.get()=='Enter Background size (1200)':
        sizeEntry.delete(0, 'end')
        sizeEntry.configure(validatecommand = (vcmd, '%P'))
def checkTextSize(_):
    if not sizeEntry.get():
        sizeEntry.configure(validatecommand = ())
        sizeEntry.insert(0, 'Enter Background size (1200)')

sizeEntry = Entry(sizeFrame, validate='all')

sizeEntry.insert(0, 'Enter Background size (1200)')
sizeEntry.grid(row= 2, column=0)

sizeEntry.bind("<FocusIn>", delTextSize)
sizeEntry.bind("<FocusOut>", checkTextSize)

#size validation/change button
def lockEntry():
    widthEntry.configure(state= DISABLED)
    heightEntry.configure(state= DISABLED)
    sizeEntry.configure(state= DISABLED)
    statusUpdate()

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
    sizeEntry.configure(state= NORMAL)
    statusUpdate()

changeButton=Button(
            sizeFrame,
            text="Change",
            fg='blue',
            command= unlockEntry
            )
changeButton.grid(row = 1, column = 1)

#directory buttons frame
dirFrame = Frame(window)
dirFrame.grid(row= 4, column= 1)

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
            command= lambda: transformation(base_dir,
                                            final_dir,
                                            window,
                                            removeVar.get(),
                                            finDirVar.get(),
                                            (widthEntry.get(),heightEntry.get()),
                                            sizeEntry.get(),
                                            clicked.get()
                                            ),
            state= DISABLED         
            )
transButton.grid(row= 5, column = 1, pady= 0)

#label for transformation status and instructions
txtStatus = StringVar()
status = Label(
    window,
    textvariable= txtStatus
)
def statusUpdate():
    if finDirVar.get():
        if base_dir.isEmpty():
            directories = "choose a directory"
        else:
            directories = ""
    else:
        if noDirectories(base_dir, final_dir):
            directories = "choose directories"
        elif yesDirectories(base_dir, final_dir):
            directories = ""
        else:
            directories = "choose a directory"
    if widthEntry['state'] == DISABLED:
        valid = ""
    else:
        valid = "validate size"

    if directories:
        directories = directories.capitalize()
        if valid:
            statusTxt = f"{directories} and {valid}."
        else:
            statusTxt = f"{directories}."
    else:
        statusTxt = valid.capitalize() + "."
    txtStatus.set(statusTxt)
    window.update()
txtStatus.set("Choose directory(ies) and validate size.")
status.grid(row= 6, column= 1, pady = 0)

window.mainloop()
