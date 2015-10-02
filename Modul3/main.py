from Modul2.gac import GAC
from Modul2.variable import Variable
from Modul2.constraintnet import  ConstraintNet
from Modul2.constraint import Constraint
from Modul2.cspstate import CspState

# TODO make a method that calculates all domains for each variable


__author__ = 'paulpm'
class Variable:
    def __init__(self,index, type, id, segments, size):
        self.size = size
        self.id = id
        self.index = index
        self.type = type
        self.segments = segments


class mod3GAC(GAC):
    def __init__(self,CNET):
        super(mod3GAC,self).__init__(CNET)
        self.rowvars=[]
        self.colvars=[]

    def generate_constraints(self):
        for rowvar in self.rowvars:
            for colvar in self.colvars:
                constraint = Constraint([rowvar, colvar], "x=y")
                self.CNET.add_constraint(rowvar, constraint)
                self.CNET.add_constraint(colvar, constraint)

    def generate_domains(self, segments, size):
        return []

    '''This revise function assumes that the domain of a variable is a list of lists containing T/F variables
    EXAMPLE:
    [
    [T,F,T,T,T,T,F,T]
    [T,T,T,T,F,F,F,F]
    [F,F,T,F,T,T,F,F]
    ]'''
    def revise(self, searchstate, statevariable, focal_constraint):
        revised = False
        for value in searchstate.domains[statevariable]:
            all_true = True
            all_false = True
            satisfies_constraint = False
            other_var = searchstate.domains[focal_constraint.get_other(statevariable)]
            for other_value in other_var:
                if len (other_var)==1:
                    if focal_constraint.function(value[other_var.index],other_value[statevariable.index]):
                        satisfies_constraint = True
                        break
                    if satisfies_constraint is False and len(other_var) ==1 :
                            searchstate.domains[statevariable].remove(value)
                            revised = True
                    elif other_value[other_var.index] is True:
                        all_false = False
                    elif other_value[statevariable.index] is False:
                        all_true = False
            if all_false:
                if value[other_var.index] is True:
                    searchstate.domains[statevariable].remove(value)
            elif all_true:
                if value[other_var.index] is False:
                    searchstate.domains[statevariable].remove(value)

        return revised


def main():
    csp = create_csp("nono-cat.txt")


def create_csp(nonogram_file):
        CNET = ConstraintNet()
        csp = mod3GAC(CNET)
        f = open("nonograms/" + nonogram_file, 'r')
        columns, rows = [int(x) for x in f.readline().strip().split(' ')]
        id_counter = 0

        for row in range(rows):
            segments =[]
            for seg in f.readline().strip().split(' '):
                segments.append(seg)
            var = Variable(row,"Row", id_counter,segments,rows-1)
            csp.variables.append(var)
            csp.rowvars.append(var)
            csp.domains[var] = csp.generate_domains(csp,segments,rows-1)

        for column in range(columns):
            segments =[]
            for seg in f.readline().strip().split(' '):
                segments.append(seg)
            var = Variable(column,"column", id_counter, segments, columns-1)
            csp.variables.append(var)
            csp.colvars.append(var)
            csp.domains[var] = csp.generate_domains(csp,segments,columns-1)

        f.close()
        return csp

if __name__ == "__main__":
    main()

