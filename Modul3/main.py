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
        self.bannedkeys =[]

    def calculate_neighbours(self, csp):
        neighbours = []
        smallest = float('inf')
        smallest_domain_key = None
        for key in self.domains.keys():
            if 1 < len(self.domains[key]) < smallest and isinstance(self.domains[key], list) and key not in \
                    self.bannedkeys:
                smallest = len(self.domains[key])
                smallest_domain_key = key
        if smallest_domain_key is None:
            return []

        for assumption in self.domains[smallest_domain_key]:
            assignment = copy.deepcopy(self.domains)
            assignment[smallest_domain_key] = [assumption]
            kid = NoNoState(assignment)
            csp.rerun(kid, smallest_domain_key)
            legal = True
            kid.calculate_heuristics()
            for key in kid.domains.keys():
                if len(kid.domains[key]) == 0:
                    legal = False
            if legal is True:
                neighbours.append(kid)


        return neighbours

    def __hash__(self):
        return hash(self.id)

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


class NonoAstarGac:

    def __init__(self,filename):
        self.csp = self.create_csp(filename)
        self.astar = Astarmod2(self.csp)
        self.generate_constraints()
        self.initialize_queue()


    def run(self):
        while len(self.astar.openlist)>0:
            self.astar.do_one_step()
        for key in self.astar.searchstate.domains.keys():
            print key, self.astar.searchstate.domains[key]



    def initialize_queue(self):
        self.csp.initialize_queue(self.astar.searchstate)

    def generate_constraints(self):
        self.csp.generate_constraints()

    def domainfilter(self):
        self.csp.domain_filter()


    def create_true_false_array(self, positionlist, lengthlist, length):
        return_array = [False]*length
        positionlist = list(positionlist)
        for i in range(len(positionlist)):
            for j in range(positionlist[i], positionlist[i] + lengthlist[i]):
                return_array[j] = True
        return return_array

    def generate_segment_domains(self,segments, length):
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

    def calculate_permutations(self,segment_domains, segments):
        permutations = list(itertools.product(*segment_domains))
        for list_element in copy.deepcopy(permutations):
            for i in range(len(list_element)-1):
                if isinstance(list_element, tuple):
                    if not list_element[i] + segments[i]  < list_element[i+1]:
                        if list_element in permutations:
                            permutations.remove(list_element)
                            break
        return permutations


    def create_csp(self,nonogram_file):
            CNET = ConstraintNet()
            csp = mod3GAC(CNET)
            f = open( nonogram_file, 'r')
            columns, rows = [int(x) for x in f.readline().strip().split(' ')]
            for row in reversed(range(rows)):
                segments = [int(x) for x in f.readline().strip().split(' ')]
                segment_domains = self.generate_segment_domains(segments, columns)
                permutations = self.calculate_permutations(segment_domains, segments)
                domain_permutations = [self.create_true_false_array(x, segments, columns) for x in permutations]
                var = Variable(row, "row", columns)
                csp.rowvars.append(var)
                csp.variables.append(var)
                csp.domains[var] = []
                for i in domain_permutations:
                    if i not in csp.domains[var]:
                        csp.domains[var].append(i)

            for column in range(columns):
                segments = [int(x) for x in f.readline().strip().split(' ')]
                segment_domains = self.generate_segment_domains(segments, rows)
                permutations = self.calculate_permutations(segment_domains, segments)
                domain_permutations = [self.create_true_false_array(x, segments, rows) for x in permutations]

                var = Variable(column, "column", columns)
                csp.colvars.append(var)
                csp.variables.append(var)
                csp.domains[var] = []
                for i in domain_permutations:
                    if i not in csp.domains[var]:
                        csp.domains[var].append(i)



            f.close()
            return csp


