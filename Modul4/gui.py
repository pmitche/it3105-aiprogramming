__author__ = 'sondredyvik'
from Tkinter import *
from board import Board

class Gui:

    def __init__(self,parent):
        self.height = 400
        self.width = 400
        self.parent = Frame(parent,width=self.width,height=self.height)
        self.canvas = Canvas(master=self.parent,width= self.width-100, height =self.height-100)
        self.canvas.pack()
        self.parent.pack()
        self.draw_board()

    def draw_board(self):
        squareheight = (self.height-100)/4
        squarewidth = (self.width-100)/4
        squaresize = min(squarewidth,squareheight)
        for x in range(5):
            for y in range(5):
                x1 = x * squaresize
                y1 = y * squaresize
                x2 = x1 + squaresize
                y2 = y1 + squaresize
                self.canvas.create_rectangle(x1,y1,x2,y2,outline="black", fill="white",
                                                                      tags="square")






root = Tk()
gui = Gui(root)
root.mainloop()