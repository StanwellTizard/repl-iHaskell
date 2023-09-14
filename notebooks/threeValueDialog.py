# author Joseph Bergin

#from tkinter import *
from tkinter import simpledialog, Label, Entry, Tk
''' Returns strings in a tuple
If you want to force int or other types, subclass this and provide
    validate(self) and getResult(self) methoda:
    
#    def getResult(self):
#        return (int(self._first.get()), int(self._second.get()), int(self._third.get()) )
#    
#    def validate(self):
#        try:
#            int(self._first.get())
#            int(self._second.get())
#            int(self._third.get())
#        except Exception as e:
#            print('invalid data - try again')
#            return False
#        return True


'''

class ThreeValueDialog(simpledialog.Dialog):
    
    def __init__(self, root, first:str, second:str, third:str, default = ('', '', '')):
        self._firstLabel = str(first)
        self._secondLabel = str(second)
        self._thirdLabel = str(third)
        ThreeValueDialog.__result = default
        super().__init__(root)

    __result = None
    
    @classmethod
    def get(cls):
        return cls.__result
        
    def getResult(self):
        return ((self._first.get()), (self._second.get()), (self._third.get()) )

    def body(self, master):
#        self.geometry('100x100')
        self.title('Police')
        
        Label(master, text=self._firstLabel).grid(row=0)
        self._first = Entry(master)
        self._first.grid(row=0, column=1)
        
        Label(master, text=self._secondLabel).grid(row=1, column=0)
        self._second = Entry(master)
        self._second.grid(row=1, column=1)
        
        Label(master, text=self._thirdLabel).grid(row=2, column=0)
        self._third = Entry(master)
        self._third.grid(row=2, column=1)
        
        return self._first # initial focus
    
    def apply(self):
        ThreeValueDialog.__result = self.getResult()
        
def dialogResult(first,second, third, default=('', '', '')):
    root = Tk()
    root.withdraw()
    ThreeValueDialog(root, first, second, third, default)
    root.destroy()
    return ThreeValueDialog.get()

if __name__ == '__main__':
    x = dialogResult('Street', 'Avenue', 'Beepers', (1, 1, 1))
    print(x)
    