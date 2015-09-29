__author__ = 'sondredyvik'

from Tkinter import *
from tkFileDialog import askopenfilename
from constraint import constraint
import csp

class csp_gui:
    def __init__(self, parent):
        self.parent = Frame(parent, width=300, height=300)
        self.parent.pack()
        csp.create_csp()




root = Tk()
gui = csp_gui(root)

root.mainloop()