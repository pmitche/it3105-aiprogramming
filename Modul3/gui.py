__author__ = 'sondredyvik'
from Tkinter import *
from tkFileDialog import askopenfilename

from main import  NonoAstarGac
class Gui:
    def __init__(self, parent,width=800, height=800 ):
        self.width = width
        self.height = height
        self.parent = Frame(parent, width =self.width, height =self.width)
        self.canvas = Canvas(master=self.parent,width= self.width, height =self.height)
        self.canvas.pack()
        self.rect_dict = {}
        self.parent.pack()


        menubar = Menu(parent)
        boardmenu = Menu(menubar, tearoff=0)
        boardmenu.add_command(label="Camel", command=lambda: self.setboard("nono-camel.txt"))
        boardmenu.add_command(label="Cat", command=lambda: self.setboard("nono-cat.txt"))
        boardmenu.add_command(label="Chick", command=lambda: self.setboard("nono-chick.txt"))
        boardmenu.add_command(label="Heart", command=lambda: self.setboard("nono-heart-1.txt"))
        boardmenu.add_command(label="Rabbit", command=lambda: self.setboard("nono-rabbit.txt"))
        boardmenu.add_command(label="Sailboat", command=lambda: self.setboard("nono-sailboat.txt"))
        boardmenu.add_command(label="Custom board", command=lambda: self.openfile())
        boardmenu.add_separator()
        boardmenu.add_command(label="Exit", command=parent.quit)
        menubar.add_cascade(label="Board", menu=boardmenu)
        parent.config(menu=menubar)

    def openfile(self):
        self.setboard(askopenfilename(parent=self.parent))

    def setboard(self,filename):
        self.canvas.delete("all")
        self.nonoastargac = NonoAstarGac(filename)
        self.drawMap()
        self.run()

    def run(self):
        self.nonoastargac.domainfilter()
        self.running = True
        self.redraw(self.nonoastargac.csp.rowvars,self.nonoastargac.csp.colvars)
        while len(self.nonoastargac.astar.openlist)>0:
            self.nonoastargac.astar.do_one_step()
        self.redraw(self.nonoastargac.csp.rowvars,self.nonoastargac.csp.colvars)


    def redraw(self,rows,cols):
        for i in range(len(cols)):
            col_list = self.nonoastargac.astar.searchstate.domains[cols[i]]
            if len(col_list) == 1:
                col_list = col_list[0]
                for j in range(len(rows)):
                    if col_list[j] is True:
                        fillcolor = "black"
                        outlinecol = "white"
                    else:
                        fillcolor = "white"
                        outlinecol ="white"
                    self.canvas.itemconfig(self.rect_dict[(i,j)],fill = fillcolor,outline=outlinecol)

    def drawMap(self):
        squarewidth =self.width/len(self.nonoastargac.csp.colvars)
        squareheight =self.height/len(self.nonoastargac.csp.rowvars)
        square_size = min(squarewidth,squareheight)
        for col in range(len(self.nonoastargac.csp.colvars)):
            for row in range(len(self.nonoastargac.csp.rowvars)):
                x1 = (col * square_size)+5
                y1 = (row * square_size)+5
                x2 = x1 + square_size
                y2 = y1 + square_size
                self.rect_dict[(col,row)] = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white",
                                                                      tags="square")


root = Tk()
gui = Gui(root)
root.mainloop()
