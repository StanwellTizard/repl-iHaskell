# author Joseph Bergin

#from tkinter import *
from tkinter import simpledialog, Label, Entry, Tk
''' The French Military Game Police Dialoog
  * @author jbergin
  Copyright 2023, Joseph Bergin 
  Educators are free to use this and adapt it for any classroom or
  training use, with attribution.It will appear shortly in the
  forthcoming "Beyond Monty Karel" by the same author. The book
  will also include and discuss a version using maps rather than
  array-like structure. This is a standard tkinter dialog 
  structure
 '''

class PoliceMove(simpledialog.Dialog):
    
    def __init__(self, root):
        super().__init__(root)

    __move = (0,0)
    
    @classmethod
    def get(cls):
        return PoliceMove.__move
        
    def getResult(self):
        return (int(self._from.get()), int(self._to.get()))

    def body(self, master):
        self.title('Police')
        
        Label(master, text="From:").grid(row=0)
        self._from = Entry(master)
        self._from.grid(row=0, column=1)
        
        Label(master, text="To:").grid(row=0, column=2)
        self._to = Entry(master)
        self._to.grid(row=0, column=3)

        return self._from # initial focus
    
    def validate(self):
        try:
            int(self._from.get())
            int(self._to.get())
        except Exception as e:
            print('invalid data - try again')
            return False
        return True
  
    def apply(self):
        PoliceMove.__move = self.getResult()
        
def policeMove():
    root = Tk()
    root.withdraw()
    PoliceMove(root)
    root.destroy()
    return PoliceMove.get()

if __name__ == '__main__':

    print(policeMove())