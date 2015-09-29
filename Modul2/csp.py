__author__ = 'paulpm, sondredyvik'
import variable
import constraint
import state

'''NOTE
Vi må gjøre så csp reduserer domenet til en spesifikk searchstate og ikke til sin egen kø eller whatever den gjør nå




'''


class CSP:

    def __init__(self):
        self.variables = []
        self.domains = {}
        self.constraints = {}
        self.queue = []

    ##Not used yet

    def makefunc(self, var_names, expression, environment=globals()):
        args = ""
        for n in var_names:
            args = args + ',' + n
        return eval('(lambda ' + args[1:] + ': ' + expression + ')', environment)

    def revise(self, searchstate, statevariable, focal_constraint):
        revised = False
        for focal_color in self.domains[statevariable]:
            satisfies_constraint = False
            for other_color in self.domains[focal_constraint.vertices[1]]:
                if focal_constraint.check_if_satisfies(focal_color,other_color):
                    satisfies_constraint = True
                    break
            if satisfies_constraint is False:
                searchstate.domains[variable].remove(focal_color)
                revised = True
        return revised

    def domain_filter(self, searchstate):
        while len(self.queue) > 0:  # While there are still tuples to be revised
            focal_variable, focal_constraint = self.queue.pop()
            if self.revise(searchstate, focal_variable, focal_constraint):
                self.add_all_tuples_in_which_variable_occurs(focal_variable, focal_constraint)

    def add_all_tuples_in_which_variable_occurs(self, state, focal_variable, focal_constraint):
        constraints_containing_variable = []
        for key, list_of_values in self.constraints.iteritems():
                    for constraint_in_list_of_values in list_of_values:
                        if focal_constraint is None:
                            if constraint_in_list_of_values.contains_variable(focal_variable):
                                constraints_containing_variable.append(constraint_in_list_of_values)
                        elif constraint_in_list_of_values.contains_variable(focal_variable) and not constraint_in_list_of_values == focal_constraint:
                            constraints_containing_variable.append(constraint_in_list_of_values)
                    for focal_constraint in constraints_containing_variable:
                        self.queue.append((focal_constraint.get_other(focal_variable),focal_constraint))
                        print focal_constraint.get_other(focal_variable),focal_constraint

    def rerun(self, state, var):
        self.add_all_tuples_in_which_variable_occurs(var, None)
        self.domain_filter(state)

    def initialize_queue(self, state):
        for variable in self.variables:  # Loop through all variables
            for focal_constraint in self.constraints[variable]:
                self.queue.append((variable, focal_constraint))


colors = ['red', 'green', 'blue', 'yellow', 'black', 'pink']


def create_csp(graph_file, domain_size):
    csp = CSP()
    f = open(graph_file, 'r')
    number_of_vertices, number_of_edges = [int(x) for x in f.readline().strip().split(' ')]

    for i in range(number_of_vertices):
        index, x, y = [i for i in f.readline().strip().split(' ')]
        vertex = variable.Variable(int(index), float(x), float(y))
        csp.variables.append(vertex)
        csp.constraints[vertex] = []

    for j in range(number_of_edges):
        i1, i2 = [int(i) for i in f.readline().strip().split(' ')]
        this_vertex = csp.variables[i1]
        other_vertex = csp.variables[i2]
        csp.constraints[this_vertex].append(constraint.Constraint([this_vertex, other_vertex]))
        csp.constraints[other_vertex].append(constraint.Constraint([other_vertex, this_vertex]))

    for k in csp.variables:
        csp.domains[k] = [colors[x] for x in range(domain_size)]

    f.close()
    return csp


def main():
    csp = create_csp("graph-color-1.txt", len(colors))
    searchstate =  generate_initial_searchstate(csp)
    csp.initialize_queue(searchstate)
    csp.domain_filter(searchstate)
    searchstate.domains[searchstate.domains.keys()[0]]= ['pink']
    csp.domain_filter(searchstate)
    for key in searchstate.domains.keys():
        print len(searchstate.domains[key])

def generate_initial_searchstate(csp):
    return state.State(csp.domains)



if __name__ == "__main__":
    main()