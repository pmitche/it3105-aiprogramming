from Modul2.gac import GAC
from common.constraintnet import ConstraintNet
from common.constraint import Constraint
from nonostate import NoNoState

__author__ = 'paulpm'


class mod3GAC(GAC):
    def __init__(self, CNET):
        super(mod3GAC, self).__init__(CNET)
        self.rowvars = []
        self.colvars = []


    def print_domain_lengths(self,domain):
        sum = 0
        for key in domain.keys():
            sum +=len( domain[key])
        print sum

    def generate_constraints(self):
        for rowvar in self.rowvars:
            for colvar in self.colvars:
                constraint = Constraint([rowvar, colvar], "x == y")
                self.CNET.add_constraint(rowvar, constraint)
                self.CNET.add_constraint(colvar, constraint)

    def generate_initial_searchstate(self):
        return NoNoState(self.domains)
    '''This revise function assumes that the domain of a variable is a list of lists containing T/F variables
    EXAMPLE:
    [
    [T,F,T,T,T,T,F,T]
    [T,T,T,T,F,F,F,F]
    [F,F,T,F,T,T,F,F]
    ]'''
    def revise(self, searchstate, statevariable, focal_constraint):
        revised = False
        for other_variable in focal_constraint.vertices:
            if other_variable != statevariable:
                boolset = set()
                for other_value in searchstate.domains[other_variable]:
                    boolset.add(other_value[statevariable.index])
                for value in searchstate.domains[statevariable]:
                    satisfies_constraint = False
                    for some_value in searchstate.domains[other_variable]:
                        if focal_constraint.function(value[other_variable.index],some_value[statevariable.index]):
                            satisfies_constraint = True
                            break
                    if not satisfies_constraint:
                        searchstate.domains[statevariable].remove(value)
                        revised = True
                    else:
                        if len(boolset) >0:
                            if not value[other_variable.index] in boolset:
                                print "here"
                                searchstate.domains[statevariable].remove(value)




        return revised