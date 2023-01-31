from tkinter  import Tk, messagebox, Checkbutton, Toplevel, IntVar, Frame, Button
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.simpledialog import askstring
from datetime import datetime
from os.path import exists
from os import makedirs, rename
from unidecode import unidecode
import sys

root = Tk()
root.title('Secrétariat')
root.withdraw() 
#Document to ask
checkList = ['Carte Identite', 'Certificat Medical', 'BNSSA', 'Recyclage BNSSA', 'PSE1', 'PSE2', 'Recyclage PSE', 'CRR', 'Permis Bateau', 'SSA', 'recyclage SSA']
#Set up range of Date
todayDate = datetime.now()
if todayDate.month < 9:
    year = todayDate.year
    yearMinusOne = (todayDate.year - 1)
    rangeYear = f"{yearMinusOne}-{year}"
else:
    year = todayDate.year
    yearPlusOne = (todayDate.year + 1)
    rangeYear = f"{year}-{yearPlusOne}"
#Ask for the name of the lifeguard
pLastName = askstring(title="Nom du sauvteur",prompt="Nom du sauveteur")
pLastName = unidecode(pLastName)
pLastName = pLastName.capitalize()
pFirstName = askstring(title="Prénom du sauvteur",prompt="Prénom du sauveteur" )
pFirstName = unidecode(pFirstName)
pFirstName = pFirstName.capitalize()
fullName = f"{pLastName}_{pFirstName}"
#ask for a folder to create folder
folderDir = askdirectory(title="Sélectionne une direction")
print(folderDir)
if not folderDir :
    exit()
dest = f"{folderDir}/{pLastName}_{pFirstName}_{rangeYear}"
if not exists(dest):
    makedirs(dest)
#ask for item to check

class Options:
    def __init__(self, parent, name, selection=None, select_all=False):
        self.parent = parent
        self.name = name
        self.selection = selection

        self.variable = IntVar()
        self.checkbutton = Checkbutton(self.parent, text=self.name,
                                       variable=self.variable, command=self.check)

        if selection is None:
            self.checkbutton.pack(side='top')
        elif select_all:
            self.checkbutton.config(command=self.select_all)
            self.checkbutton.pack()
            for item in self.selection:
                item.checkbutton.pack(side='top')

    def check(self):
        state = self.variable.get()
        if state == 1:
            print(f'Selected: {self.name}')
            checkListToAsk.append(self.name)

            if all([True if item.variable.get() == 1 else False for item in self.selection[:-1]]):
                self.selection[-1].checkbutton.select()

        elif state == 0:
            print(f'Deselected: {self.name}')
            checkListToAsk.remove(self.name)

            if self.selection[-1].variable.get() == 1:
                self.selection[-1].checkbutton.deselect()

    def select_all(self):
        state = self.variable.get()
        if state == 1:
            for item in self.selection[:-1]:
                item.checkbutton.deselect()
                item.checkbutton.invoke()
        elif state == 0:
            for item in self.selection[:-1]:
                item.checkbutton.select()
                item.checkbutton.invoke()


def ContinueFunction():    
    root.withdraw() 
    for el in checkListToAsk:
        answer = messagebox.askyesno(f"Tu veux {el} ?", f"Tu veux {el} ?")
        if answer:
            try:
                src_file  = askopenfilename(title=f"Selectionne {el}", filetypes = [("pdf",".pdf"),("All Files",".*")])
                destination = f"{dest}/{pLastName}_{pFirstName}_{el}.pdf"
                rename(src_file, destination)
            except Exception:
                sys.exit()
    sys.exit()

selection = []
checkListToAsk = []

root.deiconify()
option_frame = Frame(root)
option_frame.pack(side='left', fill='y')

for i in checkList:
    selection.append(Options(option_frame, i, selection))
selection.append(Options(option_frame, 'Select All', selection, True))

B = Button(option_frame, text ="Hello", command = ContinueFunction)

B.pack()
root.mainloop()
sys.exit()