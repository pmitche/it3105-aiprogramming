__author__ = 'paulpm, sondredyvik'

import cspstate as state
from collections import deque

'''
NOTE
Something is very odd. Probably because there is no check to see whether a search state is a success or not.
It will start iterating over the elements of a string instead.

'''
# TODO Implement functionality to check if a state is contradictory or success
# TODO fix problem in NOTE
class GAC(object):

    def __init__(self,constraintnet):
        self.CNET = constraintnet
        self.variables = []
        self.domains = {}
        self.queue = deque()

    '''
    Goes through the domain of a state and revises it

    '''
    def revise(self, searchstate, statevariable, focal_constraint):
        revised = False
        for value in searchstate.domains[statevariable]:
            satisfies_constraint = False
            for other_variable in focal_constraint.vertices:
                if other_variable != statevariable:
                    for some_value in searchstate.domains[other_variable]:
                        if focal_constraint.function(value, some_value):
                            satisfies_constraint = True
                            break
                    if not satisfies_constraint:
                        searchstate.domains[statevariable].remove(value)
                        revised = True
        return revised

    # Calls revise on elements on the queue until it is empty. Adds more to the queue if revise returns true
    def domain_filter(self):
        while len(self.queue) > 0:
            focal_state, focal_variable, focal_constraint = self.queue.popleft()
            if self.revise(focal_state, focal_variable, focal_constraint):
                self.add_all_tuples_in_which_variable_occurs(focal_state, focal_variable, focal_constraint)
    # add all vars and constraint except "this" to the queue
    def add_all_tuples_in_which_variable_occurs(self, focal_state, focal_variable, focal_constraint):
        for constraint in self.CNET.constraints[focal_variable]:
            if constraint != focal_constraint:
                for variable in constraint.get_other(focal_variable):
                    if variable != focal_variable:
                        self.queue.append((focal_state,constraint.get_other(focal_variable)[0],constraint))

    # Adds all variables affected by a constraint to the queue
    def add_all_tuples_specific_constraint(self,focal_state,focal_variable):
        for focal_constraint in self.CNET.constraints[focal_variable]:
            for other_var in focal_constraint.get_other(focal_variable):
                if other_var != focal_variable:
                    self.queue.append((focal_state, other_var, focal_constraint))

    # Adds all the pairs affected by an assumption to the queue
    # runs domain filtering on them
    def rerun(self, state, var):
        self.add_all_tuples_specific_constraint(state,var)
        self.domain_filter()
    # adds all constraint,value pairs to the queue
    def initialize_queue(self, searchstate):
        for variable in self.variables:
            for focal_constraint in self.CNET.constraints[variable]:
                self.queue.append((searchstate, variable, focal_constraint))

    def generate_initial_searchstate(self):
        return state.CspState(self.domains)

