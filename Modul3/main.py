from Modul2.gac import GAC
from Modul2.constraintnet import  ConstraintNet
from Modul2.constraint import Constraint
from Modul2.cspstate import CspState
from Modul2.astarmod2 import Astarmod2
import uuid
import itertools
import copy

__author__ = 'paulpm'





class Variable:
    def __init__(self, index, type, size):
        self.size = size
        self.index = index
        self.type = type

    def __repr__(self):
        return str(self.type)+ str(self.index)

    def __eq__(self, other):
        return self.size == other.size and self.index == other.index and self.type == other.type

    def __hash__(self):
        return hash(str(self.type)+ str(self.index))


class NoNoState(CspState):
    def __init__(self, domains):
        super(NoNoState,self).__init__(domains)
        self.id = uuid.uuid4()

    def __hash__(self):
        return hash(self.id)

class mod3GAC(GAC):
    def __init__(self, CNET):
        super(mod3GAC, self).__init__(CNET)
        self.rowvars = []
        self.colvars = []


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
    def revise(self, searchstate, focal_variable, focal_constraint):
        other_var = focal_constraint.get_other(focal_variable)[0]
        this_index = focal_variable.index
        other_index = other_var.index
        other_var_domain = searchstate.domains[other_var]
        revised = False
        for this_value in copy.deepcopy(searchstate.domains[focal_variable]):
            all_true = True
            all_false = True
            breaks_constraints = False
            for other_value in other_var_domain:
                if len(other_var_domain) ==1:
                    if not focal_constraint.function(this_value[other_var.index], other_value[focal_variable.index]):
                        breaks_constraints = True
                        break
                else:
                    if other_value[this_index] is False:
                        all_true = False
                    elif other_value[this_index] is True:
                        all_false = False
            if all_true:
                if this_value[other_index] is False:
                    breaks_constraints = True

            elif all_false:
                if this_value[other_index] is True:
                    breaks_constraints = True
            if breaks_constraints:
                print this_value
                searchstate.domains[focal_variable].remove(this_value)

        return revised








def main():
    csp = create_csp("nono-cat.txt")
    csp.generate_constraints()
    astar = Astarmod2(csp)
    csp.initialize_queue(astar.searchstate)
    csp.domain_filter()
    sum = 0
    for key in astar.searchstate.domains.keys():
        sum += len(astar.searchstate.domains[key])
       # print key, astar.searchstate.domains[key]
    print sum

    astar.do_one_step()
    astar.do_one_step()
    astar.do_one_step()
    sum = 0
    for key in astar.searchstate.domains.keys():
        sum += len(astar.searchstate.domains[key])
        #print key, astar.searchstate.domains[key]
    print sum




def create_true_false_array(positionlist, lengthlist, length):
    return_array = [False]*length
    positionlist = list(positionlist)
    for i in range(len(positionlist)):
        for j in range(positionlist[i], positionlist[i] + lengthlist[i]):
            return_array[j] = True
    return return_array




def generate_segment_domains(segments, length):
    segment_start_ranges = [0]
    segment_end_ranges = []
    start_total = 0

    for i in range(1, len(segments)):
        start_total += segments[i-1] + 1
        segment_start_ranges.append(start_total)

    for j in range(0, len(segments)):
        end_total = length + 1
        for k in range(j, len(segments)):
            end_total -= segments[k] + 1
        segment_end_ranges.append(end_total)

    segment_domains = []
    for k in range(len(segments)):
        segment_domains.append([x for x in range(segment_start_ranges[k], segment_end_ranges[k]+1)])

    return segment_domains


def calculate_permutations(segment_domains, segments):
    permutations = list(itertools.product(*segment_domains))
    for list_element in permutations:
        for i in range(len(list_element)-1):
            if isinstance(list_element, list):
                if not list_element[i] + segments[i] + 1 < list_element[i]:
                    permutations.remove(list_element)
    return permutations


def create_csp(nonogram_file):
        CNET = ConstraintNet()
        csp = mod3GAC(CNET)
        f = open("nonograms/" + nonogram_file, 'r')
        columns, rows = [int(x) for x in f.readline().strip().split(' ')]

        for row in range(rows):
            segments = [int(x) for x in f.readline().strip().split(' ')]
            segment_domains = generate_segment_domains(segments, columns)
            permutations = calculate_permutations(segment_domains, segments)
            domain_permutations = [create_true_false_array(x, segments, columns) for x in permutations]

            var = Variable(row, "row", columns)
            csp.rowvars.append(var)
            csp.variables.append(var)
            csp.domains[var] = domain_permutations

        for column in range(columns):
            segments = [int(x) for x in f.readline().strip().split(' ')]
            segment_domains = generate_segment_domains(segments, rows)
            permutations = calculate_permutations(segment_domains, segments)
            domain_permutations = [create_true_false_array(x, segments, rows) for x in permutations]

            var = Variable(column, "column", columns)
            csp.colvars.append(var)
            csp.variables.append(var)
            csp.domains[var] = domain_permutations


        f.close()
        return csp



if __name__ == "__main__":
    main()

