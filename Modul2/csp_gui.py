__author__ = 'sondredyvik'

from Tkinter import *
from tkFileDialog import askopenfilename
from csp import CSP
import variable as cspvariable
import constraint as cspconstraint
import astarmod2

class csp_gui:
    def __init__(self, parent):
        self.parent = Frame(parent, width=500, height=500)
        self.vertex_dict = {}
        self.edge_dict = {}
        self.colors = [0, 1, 2, 3, 4, 5]
        self.number_to_color ={0: 'black', 1: "yellow", 2: "pink", 3: "purple", 4: "red", 5: "blue"}
        self.csp = self.create_csp("graph-color-1.txt", 4)
        self.canvas = Canvas(master=self.parent,width=500, height=500)
        self.canvas.pack()
        self.parent.pack()
        self.drawmap()
        self.astar = astarmod2.Astarmod2(self.csp)
        self.csp.initialize_queue(self.astar.searchstate)
        self.csp.domain_filter()
        self.run_astar()

    def normalize_coordinates(self,xpos,ypos):
        highestx = max([float(var.x) for var in self.csp.variables])
        lowestx = min([float(var.x )for var in self.csp.variables])
        highesty = max([float(var.y) for var in self.csp.variables])
        lowesty = min([float(var.y )for var in self.csp.variables])
        old_range =float(highestx-lowestx)
        new_range = float(480-20)
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
            self.parent.after(300, lambda: self.run_astar())
        else:
            for key in self.astar.searchstate.domains.keys():
                self.canvas.itemconfig(self.vertex_dict[key.index], fill=self.number_to_color[self.astar.searchstate.domains[key][0]])
            for key in self.csp.constraints.keys():
                for constraint in self.csp.constraints[key]:
                    if self.astar.searchstate.domains[constraint.vertices[0]] ==self.astar.searchstate.domains[constraint.vertices[1]]:
                        print "suckadickanddie",  self.astar.searchstate.domains[constraint.vertices[0]], self.astar.searchstate.domains[constraint.vertices[1]]





    def drawmap(self):
        self.vertex_dict = {}
        self.edge_dict = {}
        self.canvas.delete('oval')
        for key in self.csp.constraints.keys():
            for constraint in self.csp.constraints[key]:
                x1,y1 = self.normalize_coordinates(constraint.vertices[0].x, constraint.vertices[0].y)
                x2,y2 = self.normalize_coordinates(constraint.vertices[1].x, constraint.vertices[1].y)
                Canvas.create_line(self.canvas,x1,y1,x2,y2)
        for variable in self.csp.variables:
            x1,y1 = self.normalize_coordinates(variable.x, variable.y)
            x1 = x1-10
            y1 = y1 -10
            x2 = x1 +20
            y2 = y1 +20
            self.vertex_dict[variable.index] = Canvas.create_oval(self.canvas, x1, y1, x2, y2)









    def create_csp(self,graph_file, domain_size):
        csp = CSP()
        f = open(graph_file, 'r')
        number_of_vertices, number_of_edges = [int(x) for x in f.readline().strip().split(' ')]

        for i in range(number_of_vertices):
            index, x, y = [i for i in f.readline().strip().split(' ')]
            vertex = cspvariable.Variable(int(index), float(x), float(y))
            csp.variables.append(vertex)
            csp.constraints[vertex] = []

        for j in range(number_of_edges):
            i1, i2 = [int(i) for i in f.readline().strip().split(' ')]
            this_vertex = csp.variables[i1]
            other_vertex = csp.variables[i2]
            csp.constraints[this_vertex].append(cspconstraint.Constraint([this_vertex, other_vertex]))
            csp.constraints[other_vertex].append(cspconstraint.Constraint([other_vertex, this_vertex]))

        for k in csp.variables:
            csp.domains[k] = [self.colors[x] for x in range(domain_size)]

        f.close()
        return csp





root = Tk()
gui = csp_gui(root)

root.mainloop()

