__author__ = 'paulpm, sondredyvik'
import variable as cspvariable
import constraint as cspconstraint
import state
from collections import deque
import astarmod2
'''
NOTE
Something is very odd. Probably because there is no check to see whether a search state is a success or not.
It will start iterating over the elements of a string instead.

'''
# TODO Implement functionality to check if a state is contradictory or success
# TODO fix problem in NOTE
class CSP:
    #Initialises the csp

    def __init__(self):
        self.variables = []
        self.domains = {}
        self.constraints = {}
        self.queue = deque()


    def makefunc(self, var_names, expression, environment=globals()):
        args = ""
        for n in var_names:
            args = args + ',' + n
        return eval('(lambda ' + args[1:] + ': ' + expression + ')', environment)
    '''
    Goes through the domain of a state and revises it

    '''
    def revise(self, searchstate, statevariable, focal_constraint):
        revised = False
        for value in searchstate.domains[statevariable]:
            satisfies_constraint = False
            for other_variable in focal_constraint.get_other(statevariable):
                for some_value in searchstate.domains[other_variable]:
                    if focal_constraint.check_if_satisfies(value,some_value):
                        satisfies_constraint = True
                        break
                if not satisfies_constraint:
                    searchstate.domains[statevariable].remove(value)
                    revised = True
        return revised


    def domain_filter(self):
        while len(self.queue) > 0:
            focal_state, focal_variable, focal_constraint = self.queue.popleft()
            if self.revise(focal_state, focal_variable, focal_constraint):
                self.add_all_tuples_in_which_variable_occurs(focal_state, focal_variable, focal_constraint)

    def add_all_tuples_in_which_variable_occurs(self, focal_state, focal_variable, focal_constraint):
        for constraint in self.constraints[focal_variable]:
            if not constraint == focal_constraint:
                for other_var in focal_constraint.get_other(focal_variable):
                    self.queue.append((focal_state, other_var, focal_constraint))


    def add_all_tuples_specific_constraint(self,focal_state,focal_variable):
        for focal_constraint in self.constraints[focal_variable]:
            for other_var in focal_constraint.get_other(focal_variable):
                self.queue.append((focal_state, other_var, focal_constraint))


    def rerun(self, state, var):
        self.add_all_tuples_specific_constraint(state,var)
       # for element in self.queue:
       #     print element[1],element[2]
        self.domain_filter()

    def initialize_queue(self, searchstate):
        for variable in self.variables:
            for focal_constraint in self.constraints[variable]:
                self.queue.append((searchstate, variable, focal_constraint))

    def generate_initial_searchstate(self):
        return state.State(self.domains)





colors = [0,1,2,3,4,5,6]


def create_csp(graph_file, domain_size):
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
        csp.domains[k] = [colors[x] for x in range(domain_size)]

    f.close()
    return csp


def main():
    csp = create_csp("graph-color-1.txt", 4)
    astar = astarmod2.Astarmod2(csp)
    csp.initialize_queue(astar.searchstate)
    csp.domain_filter()
    while len(astar.openlist)>0:
        astar.do_one_step()
    for key in astar.searchstate.domains.keys():
        for constraint in csp.constraints[key]:
            print key, astar.searchstate.domains[key], constraint, constraint.get_other(key)[0]\
                , astar.searchstate.domains[constraint.get_other(key)[0]]




def generate_initial_searchstate(csp):
    return state.State(csp.domains)



if __name__ == "__main__":
    main()