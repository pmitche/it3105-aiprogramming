from Modul2.gac import GAC
from Modul2.variable import Variable
from Modul2.constraintnet import  ConstraintNet
from Modul2.constraint import Constraint
from Modul2.cspstate import CspState
import itertools

# TODO make a method that calculates all domains for each variable


__author__ = 'paulpm'
class Variable:
    def __init__(self,index, type, id, segments, size):
        self.size = size
        self.id = id
        self.index = index
        self.type = type
        self.segments = segments

class Segment:
    def __init__(self, index, size, row_num, col_num):
        self.index = index
        self.size = size
        self.row_num = row_num
        self.col_num = col_num

    def __repr__(self):
        if self.row_num == -1:
            return str(self.index) + "col" + str(self.col_num) + "-" + str(self.size)
        return str(self.index) + "row" + str(self.row_num) + "-" + str(self.size)


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
            segments = []
            segment_start_ranges = [0]
            segment_end_ranges = []
            segment_domains = []
            start_total = 0
            for size in f.readline().strip().split(' '):
                segments.append(int(size))
            for i in range(1, len(segments)):
                start_total += segments[i-1] + 1
                segment_start_ranges.append(start_total)
            for j in range(0, len(segments)):
                end_total = columns + 1
                for k in range(j, len(segments)):
                    end_total -= segments[k] + 1
                segment_end_ranges.append(end_total)
            for i in range(len(segments)):
                    segment_domains.append([x for x in range(segment_start_ranges[i], segment_end_ranges[i]+1)])
            print "Row " + str(row) + ": " + str(segment_domains)
            permutations = list(itertools.product(*segment_domains))
            for list_element in permutations:
                for i in range(len(list_element)-1):
                    if isinstance(list_element, list):
                        if not list_element[i] + segments[i] + 1 < list_element[i]:
                            permutations.remove(list_element)
            print permutations
            #true_false = [[True for i in range(columns)] for j in range(segment_start_ranges[j], segment_end_ranges[j]+1) ]
            #print true_false





            for k in range(len(segments)):
                s = Segment(id_counter, segments[k], row, -1)
                id_counter += 1
                csp.variables.append(s)
                #csp.constraints[s] = []
                csp.domains[s] = [int(x) for x in range(segment_start_ranges[k], segment_end_ranges[k]+1)]

            for k in range(1, len(segments)):
                """csp.constraints[csp.variables[id_counter-1]].append(
                    Constraint([csp.variables[id_counter-1], csp.variables[id_counter-2]],
                               str(csp.variables[id_counter-1]) + ">" + str(csp.variables[id_counter-2]) + "+" +
                               str(len(csp.domains[csp.variables[id_counter-2]]))))"""

        for column in range(columns):
            segments = []
            segment_start_ranges = [0]
            segment_end_ranges = []
            start_total = 0
            for size in f.readline().strip().split(' '):
                segments.append(int(size))
            for i in range(1, len(segments)):
                start_total += segments[i-1] + 1
                segment_start_ranges.append(start_total)
            for j in range(0, len(segments)):
                end_total = rows + 1
                for k in range(j, len(segments)):
                    end_total -= segments[k] + 1
                segment_end_ranges.append(end_total)
            print "Col " + str(column) + ": " + str(segment_start_ranges), str(segment_end_ranges)

            for k in range(len(segments)):
                s = Segment(id_counter, segments[k], -1, column)
                id_counter += 1
                csp.variables.append(s)
                #csp.constraints[s] = []
                csp.domains[s] = [int(x) for x in range(segment_start_ranges[k], segment_end_ranges[k]+1)]

            for k in range(1, len(segments)):
                """csp.constraints[csp.variables[id_counter-1]].append(
                    Constraint([csp.variables[id_counter-1], csp.variables[id_counter-2]],
                               str(csp.variables[id_counter-1]) + ">" + str(csp.variables[id_counter-2]) + "+" +
                               str(len(csp.domains[csp.variables[id_counter-2]]))))"""


        # TODO: Implement method to calculate initial reduced domain using arithmetic
        # TODO: Populate csp.constraints with constraints on the form segmentA.start + segmentA.size > segmentB.start

        print "CSP variables: " + str(csp.variables)
        print "-------------------------------------------------------------"
        #print "CSP constraints: " + str(csp.constraints)
        print "-------------------------------------------------------------"
        print "CSP domains: " + str(csp.domains)

        f.close()
        return csp

if __name__ == "__main__":
    main()

