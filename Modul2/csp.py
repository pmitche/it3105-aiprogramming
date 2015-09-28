__author__ = 'paulpm'

""" NOTE:
    Classes Constraint, Vertex and CSP should go into constraint.py, vertex.py and csp.py respectively.
    They are all in this class only during the initial stages of development.
"""


class Constraint:
    def __init__(self, vertices):
        self.vertices = vertices

    def __repr__(self):
        return str((self.vertices[0],self.vertices[1]))

    def __eq__(self, other):
        return self.vertices[0] == other.vertices[0] and self.vertices[1] == other.vertices[1]

    def contains_variable(self, variable):
        return self.vertices[0] == variable or self.vertices[1] == variable

    def get_other(self,var):
        if self.vertices[0] == var:
            return self.vertices[1]
        if self.vertices[1] == var:
            return self.vertices[0]
        else:
            raise AttributeError





class Variable:

    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y

    def __repr__(self):
        return 'n' + str(self.index)

    def __hash__(self):
        return hash((self.index, self.x, self.y))

    def __eq__(self, other):
        return self.index == other.index


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

    def revise(self, variable, constraint):
        revised = False
        for focal_color in self.domains[variable]:
            satisfies_constraint = False
            for other_color in self.domains[constraint.vertices[1]]:
                if not focal_color == other_color:
                    satisfies_constraint = True
                    break
            if satisfies_constraint is False:
                self.domains[variable].remove(focal_color)
                revised = True
        return revised

    def domain_filter(self):
        while len(self.queue) > 0:  # While there are still tuples to be revised
            var, const = self.queue.pop()
            return_value = self.revise(var, const)
            constraints_containing_variable = []
            if return_value is True:
                for key, value in self.constraints.iteritems():
                    if value.contains_variable(var) and not value == const:
                        constraints_containing_variable.append(value)
                for constraint in constraints_containing_variable:
                    self.queue.append((constraint.get_other(var),constraint))

    def rerun(self, focal_variable):
        self.queue.append((focal_variable, self.constraints[focal_variable]))
        self.domain_filter()

    def initialize_queue(self):
        for variable in self.variables:  # Loop through all variables
            for constraint in self.constraints[variable]:
                self.queue.append((variable, constraint))


colors = ['red', 'green', 'blue', 'yellow', 'black', 'pink']


def create_csp(graph_file, domain_size):
    csp = CSP()
    f = open(graph_file, 'r')
    number_of_vertices, number_of_edges = [int(x) for x in f.readline().strip().split(' ')]

    for i in range(number_of_vertices):
        index, x, y = [i for i in f.readline().strip().split(' ')]
        vertex = Variable(int(index), float(x), float(y))
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
    csp = create_csp("graph-color-1.txt", len(colors))
    csp.initialize_queue()
    csp.domain_filter()
    csp.domains[csp.domains.keys()[0]] = ['pink']
    csp.domain_filter()
    print [len(csp.domains[key]) for  key in csp.domains.keys()]


if __name__ == "__main__":
    main()