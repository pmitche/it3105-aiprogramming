__author__ = 'sondredyvik'

from Tkinter import *
from tkFileDialog import askopenfilename
from csp import CSP
import variable as cspvariable
import constraint as cspconstraint


class csp_gui:
    def __init__(self, parent):
        self.parent = Frame(parent, width=500, height=500)
        self.colors =[0,1,2,3,4,5]
        self.csp = self.create_csp("graph-color-1.txt", 6)
        self.canvas = Canvas(master=self.parent,width=500, height=500)
        self.parent.pack()
    def drawmap(self):
        self.vertex_dict ={}



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

