__author__ = 'sondredyvik'

from Tkinter import *
from tkFileDialog import askopenfilename
from gac import GAC
import variable as cspvariable
import constraint as cspconstraint
import constraintnet
import astarmod2
import time
import gc

class csp_gui:
    def __init__(self, parent):
        self.width = 800
        self.height = 800
        self.parent = Frame(parent, width =self.width, height =self.width)
        self.vertex_dict = {}
        self.edge_dict = {}
        self.colors = [0, 1, 2, 3, 4, 5, 6, 7]
        self.number_to_color = {0: 'blue', 1: "green", 2: "yellow", 3: "chocolate", 4: "dark khaki", 5: "seashell2",
                                6: "red", 7: "cadet blue"}
        self.csp = None
        self.canvas = Canvas(master=self.parent,width= self.width, height =self.height)
        self.canvas.pack()
        self.parent.pack()
        self.board = None
        self.CNET = None
        self.running = False


        menubar = Menu(parent)
        boardmenu = Menu(menubar, tearoff=0)
        boardmenu.add_command(label="Board 1", command=lambda: self.setboard("graph-color-1.txt"))
        boardmenu.add_command(label="Board 2", command=lambda: self.setboard("graph-color-2.txt"))
        boardmenu.add_command(label="Board 3", command=lambda: self.setboard("rand-50-4-color1.txt"))
        boardmenu.add_command(label="Board 4", command=lambda: self.setboard("rand-100-4-color1.txt"))
        boardmenu.add_command(label="Board 5", command=lambda: self.setboard("rand-100-6-color1.txt"))
        boardmenu.add_command(label="Board 6", command=lambda: self.setboard("spiral-500-4-color1.txt"))
        boardmenu.add_command(label="Custom board", command=lambda: self.openfile())
        boardmenu.add_separator()
        boardmenu.add_command(label="Exit", command=parent.quit)
        menubar.add_cascade(label="Board", menu=boardmenu)

        k_menu = Menu(menubar, tearoff=0)
        k_menu.add_command(label="K=1", command=lambda: self.run(1))
        k_menu.add_command(label="K=2", command=lambda: self.run(2))
        k_menu.add_command(label="K=3", command=lambda: self.run(3))
        k_menu.add_command(label="K=4", command=lambda: self.run(4))
        k_menu.add_command(label="K=5", command=lambda: self.run(5))
        k_menu.add_command(label="K=6", command=lambda: self.run(6))
        k_menu.add_command(label="K=7", command=lambda: self.run(7))
        k_menu.add_command(label="K=8", command=lambda: self.run(8))
        menubar.add_cascade(label="Colors", menu=k_menu)

        speedmenu = Menu(menubar,tearoff=0)
        speedmenu.add_command()

        parent.config(menu=menubar)

    def openfile(self):
        self.setboard(askopenfilename(parent=self.parent))

    def setboard(self,filename):
        self.board = filename

    def run(self,k):
        if self.running is False:
            if self.board is None:
                self.setboard("graph-color-1")
            self.canvas.delete("all")
            self.running = True
            self.csp = self.create_csp(self.board, k)
            self.drawmap()
            self.astar = astarmod2.Astarmod2(self.csp)
            self.csp.initialize_queue(self.astar.searchstate)
            self.csp.domain_filter()
            self.time = time.time()
            self.run_astar()

    def normalize_coordinates(self,xpos,ypos):
        highestx = max([float(var.x) for var in self.csp.variables])
        lowestx = min([float(var.x )for var in self.csp.variables])
        highesty = max([float(var.y) for var in self.csp.variables])
        lowesty = min([float(var.y )for var in self.csp.variables])
        old_range =float(highestx-lowestx)
        new_range = float(self.width-20)
        new_x = (((float(xpos)-lowestx)*new_range)/old_range) + 20
        old_range = float(highesty-lowesty)
        new_y = (((float(ypos)-lowesty)*new_range)/old_range) + 20
        return new_x, new_y


    def run_astar(self):
        self.astar.do_one_step()
        for key in self.astar.searchstate.domains.keys():
            if len(self.astar.searchstate.domains[key]) == 1:
                self.canvas.itemconfig(self.vertex_dict[key.index], fill=self.number_to_color[self.astar.searchstate.domains[key][0]])
        if len(self.astar.openlist)> 0:
            self.parent.after(1, lambda: self.run_astar())
        else:
            for key in self.astar.searchstate.domains.keys():
                if len(self.astar.searchstate.domains[key]) == 1:
                    self.canvas.itemconfig(self.vertex_dict[key.index], fill=self.number_to_color[self.astar.searchstate.domains[key][0]])
                else:
                    self.canvas.itemconfig(self.vertex_dict[key.index], fill="white")
            for key in self.CNET.constraints.keys():
                for constraint in self.CNET.constraints[key]:
                    if self.astar.searchstate.domains[constraint.vertices[0]] ==self.astar.searchstate.domains[constraint.vertices[1]]:
                        Canvas.create_text(self.canvas, 400, 400, fill="red", text="NO SOLUTION FOUND")
            print "DONE"
            print time.time() - self.time
            self.running = False


    def drawmap(self):
        self.vertex_dict = {}
        self.edge_dict = {}
        self.canvas.delete('oval')
        for key in self.CNET.constraints.keys():
            for constraint in self.CNET.constraints[key]:
                x1,y1 = self.normalize_coordinates(constraint.vertices[0].x, constraint.vertices[0].y)
                x2,y2 = self.normalize_coordinates(constraint.vertices[1].x, constraint.vertices[1].y)
                Canvas.create_line(self.canvas,x1,y1,x2,y2)
        for variable in self.csp.variables:
            x1,y1 = self.normalize_coordinates(variable.x, variable.y)
            x1 = x1-10
            y1 = y1 -10
            x2 = x1 +20
            y2 = y1 +20
            self.vertex_dict[variable.index] = Canvas.create_oval(self.canvas, x1, y1, x2, y2, fill="white")







    def create_csp(self,graph_file, domain_size):
        self.CNET = constraintnet.ConstraintNet()
        gac = GAC(self.CNET)
        f = open(graph_file, 'r')
        number_of_vertices, number_of_edges = [int(x) for x in f.readline().strip().split(' ')]

        for i in range(number_of_vertices):
            index, x, y = [i for i in f.readline().strip().split(' ')]
            vertex = cspvariable.Variable(int(index), float(x), float(y))
            gac.variables.append(vertex)

        for j in range(number_of_edges):
            i1, i2 = [int(i) for i in f.readline().strip().split(' ')]
            this_vertex = gac.variables[i1]
            other_vertex = gac.variables[i2]
            constraint = cspconstraint.Constraint([this_vertex, other_vertex], "x!=y")
            self.CNET.add_constraint(this_vertex,constraint)
            self.CNET.add_constraint(other_vertex,constraint)



        for k in gac.variables:
            gac.domains[k] = [self.colors[x] for x in range(domain_size)]

        f.close()
        return gac





root = Tk()
gui = csp_gui(root)

root.mainloop()

