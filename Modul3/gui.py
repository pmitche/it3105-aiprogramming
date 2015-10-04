__author__ = 'sondredyvik'
from Tkinter import *
from tkFileDialog import askopenfilename

from nonogram import NonoAstarGac
class Gui:
    def __init__(self, parent,width=800, height=800 ):
        self.width = width
        self.height = height
        self.parent = Frame(parent, width =self.width, height =self.width)
        self.canvas = Canvas(master=self.parent,width= self.width, height =self.height)
        self.canvas.pack()
        self.rect_dict = {}
        self.parent.pack()
        self.running = False


        menubar = Menu(parent)
        boardmenu = Menu(menubar, tearoff=0)
        boardmenu.add_command(label="Camel", command=lambda: self.setboard("nonograms/nono-camel.txt"))
        boardmenu.add_command(label="Cat", command=lambda: self.setboard("nonograms/nono-cat.txt"))
        boardmenu.add_command(label="Chick", command=lambda: self.setboard("nonograms/nono-chick.txt"))
        boardmenu.add_command(label="Heart", command=lambda: self.setboard("nonograms/nono-heart-1.txt"))
        boardmenu.add_command(label="Rabbit", command=lambda: self.setboard("nonograms/nono-rabbit.txt"))
        boardmenu.add_command(label="Sailboat", command=lambda: self.setboard("nonograms/nono-sailboat.txt"))
        boardmenu.add_command(label="Telephone", command=lambda: self.setboard("nonograms/nono-telephone.txt"))
        boardmenu.add_command(label="Custom board", command=lambda: self.openfile())
        boardmenu.add_separator()
        boardmenu.add_command(label="Exit", command=parent.quit)
        menubar.add_cascade(label="Board", menu=boardmenu)
        parent.config(menu=menubar)

    def openfile(self):
        self.setboard(askopenfilename(parent=self.parent))

    def setboard(self,filename):
        self.running= False
        self.canvas.delete("all")
        self.nonoastargac = NonoAstarGac(filename)
        self.drawMap()
        self.run()
    def do_one_astar_step(self):
        self.nonoastargac.astar.do_one_step()
        self.redraw(self.nonoastargac.csp.rowvars,self.nonoastargac.csp.colvars)


    def run(self):
        if not self.running:
            self.nonoastargac.domainfilter()
            self.running = True
            self.redraw(self.nonoastargac.csp.rowvars,self.nonoastargac.csp.colvars)
        if self.running:
            self.nonoastargac.astar.do_one_step()
            self.redraw(self.nonoastargac.csp.rowvars,self.nonoastargac.csp.colvars)

        if len(self.nonoastargac.astar.openlist)>0:
            self.parent.after(100, self.run)

        print "nodes created: " + str(self.nonoastargac.astar.nodes_created)
        print "nodes expanded: " +str(self.nonoastargac.astar.nodes_expanded)
        print "length of path: "+ str(len(self.nonoastargac.astar.findpath(self.nonoastargac.astar.searchstate)))




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
        for i in (range(len(rows))):
            row_list = self.nonoastargac.astar.searchstate.domains[rows[i]]
            if len(row_list) == 1:
                row_list = row_list[0]
                for j in range(len(rows)-1):
                    if row_list[j] is True:
                        fillcolor = "black"
                        outlinecol = "white"
                    else:
                        fillcolor = "white"
                        outlinecol ="white"

                    self.canvas.itemconfig(self.rect_dict[(j,len(rows)-1-i)],fill = fillcolor,outline=outlinecol)

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
