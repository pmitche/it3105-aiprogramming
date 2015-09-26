__author__ = 'paulpm'

""" NOTE:
    Classes Constraint, Vertex and CSP should go into constraint.py, vertex.py and csp.py respectively.
    They are all in this class only during the initial stages of development.
"""
import variable

class Constraint:

    def __init__(self, vertices):
        self.vertices = vertices


class Vertex:

    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y

    def __repr__(self):
        return 'n' + str(self.index)


class CSP:

    def __init__(self):
        self.variables = []
        self.domains = {}
        self.constraints = {}
        self.queue = []

    def makefunc(self, var_names, expression, environment=globals()):
        args = ""
        for n in var_names:
            args = args + ',' + n
        return eval('(lambda ' + args[1:] + ': ' + expression + ')', environment)

    def revise(self,variable,constraint):
        #maybe not very efficient
        newdomain = []
        for focal_color in self.domains[variable]:
            for other_color in self.domains[constraint]:
                if not focal_color == other_color:
                    newdomain.append(focal_color)
        if not len(newdomain) == len(self.domains[variable]):
            self.domains[variable] = newdomain
            return True
        return False

    def domain_filter(self):
        while len(self.queue) > 0:
            var,const = self.queue.pop()
            returnval = self.revise(var,const)
            if returnval:
                for constraint in self.constraints[var]:
                    self.queue.append(constraint,self.constraints[constraint])

    def rerun(self,focal_variable):
        self.queue.append(focal_variable,self.constraints[focal_variable])
        self.domain_filter()

    def initialize_queue(self):
        for variable in self.variables:
            for constraint in variable.constraints:
                self.queue.append(variable,constraint)


colors = ['red', 'green', 'blue', 'yellow', 'black', 'pink']


def create_csp(graph_file, domain_size):
    csp = CSP()
    f = open(graph_file, 'r')
    number_of_vertices, number_of_edges = [int(x) for x in f.readline().strip().split(' ')]

    for i in range(number_of_vertices):
        index, x, y = [i for i in f.readline().strip().split(' ')]
        vertex = Vertex(int(index), float(x), float(y))
        csp.variables.append(vertex)
        csp.constraints[vertex] = []

    for j in range(number_of_edges):
        i1, i2 = [int(i) for i in f.readline().strip().split(' ')]
        this_vertex = csp.variables[i1]
        other_vertex = csp.variables[i2]
        csp.constraints[this_vertex].append(Constraint([this_vertex, other_vertex]))
        csp.constraints[other_vertex].append(Constraint([other_vertex, this_vertex]))

    for k in csp.variables:
        csp.domains[k] = [colors[x] for x in range(domain_size)]

    f.close()
    return csp


def main():
    create_csp("graph-color-1.txt", len(colors))

if __name__ == "__main__":
    main()


