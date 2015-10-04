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
        print "hei"
        neighbours = []
        smallest = float('inf')
        smallest_domain_key = None
        for key in self.domains.keys():
            if 1 < len(self.domains[key]) < smallest and isinstance(self.domains[key], list):
                smallest = len(self.domains[key])
                smallest_domain_key = key

        for assumption in self.domains[smallest_domain_key]:
            assignment = copy.deepcopy(self.domains)
            assignment[smallest_domain_key] = [assumption]
            kid = NoNoState(assignment)
            print "BEFORE-------------"
            for key in kid.domains.keys():
                     print key, kid.domains[key]
            csp.rerun(kid, smallest_domain_key)
            print "AFTER-------------"
            for key in kid.domains.keys():
                     print key, kid.domains[key]
            legal = True
            kid.calculate_heuristics()
            for key in kid.domains.keys():
                if len(kid.domains[key]) == 0:
                    legal = False
            if legal is True:
                neighbours.append(kid)
                for key in kid.domains.keys():
                     print key, kid.domains[key]
        print len(neighbours)

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
    def revise(self, searchstate, focal_variable, focal_constraint):
        # other_var = focal_constraint.get_other(focal_variable)[0]
        # other_index = other_var.index
        # other_var_domain = searchstate.domains[other_var]
        # this_var = focal_variable
        # this_index =this_var.index
        # satisfies_constraint = False
        # this_var_domain = searchstate.domains[this_var]
        # check_if_satisfies = focal_constraint.function
        # for focal_combination in this_var_domain:
        #     all_true = True
        #     all_false = True
        #     for other_combination in other_var_domain:
        #         if len(other_var_domain)==1:
        #             if check_if_satisfies(focal_combination[other_index], other_combination[this_index]):
        #                 satisfies_constraint = True
        #                 break
        #         elif other_combination[this_index] is False:
        #             all_true = False
        #         elif other_combination[this_index] is True:
        #             all_false = False
        #     if all_true and focal_combination[other_index] is False and len(other_var_domain)>1:
        #         this_var_domain.remove(focal_combination)
        #         return True
        #     if all_false and focal_combination[other_index] is True and len(other_var_domain)>1:
        #         this_var_domain.remove(focal_combination)
        #         return True
        #
        #
        # return False
        #




        other_var = focal_constraint.get_other(focal_variable)[0]
        this_index = focal_variable.index
        this_var_domain = searchstate.domains[focal_variable]
        other_index = other_var.index
        other_var_domain = searchstate.domains[other_var]
        check_if_satisfies = focal_constraint.function
        all_true = True
        all_false = True
        for other_combination in other_var_domain:
            if other_combination[this_index] == False:
                all_true = False
            elif other_combination[this_index]==True:
                all_false = False
        for this_combination in this_var_domain:
            if all_false and this_combination[other_index] == True:
               this_var_domain.remove(this_combination)
               return True
            if all_true and this_combination[other_index] == False:
                this_var_domain.remove(this_combination)
                return True
                print (this_combination[other_index]), focal_variable
            if all_false and all_true:
                print "something is very wrong"
            for other_combination in other_var_domain:
                if len(other_var_domain)==1:
                    pass
        for this_combination in this_var_domain:
            for other_combination in other_var_domain:
                if len(other_var_domain) == 1:
                    if not check_if_satisfies(this_combination[other_index],other_combination[this_index]):
                        print check_if_satisfies(this_combination[other_index],other_combination[this_index])
                        print this_combination in this_var_domain, "heir"
                        this_var_domain.remove(this_combination)
                        return True
        return False




def main():
    csp = create_csp("nono-cat.txt")
    csp.generate_constraints()
    astar = Astarmod2(csp)
    csp.initialize_queue(astar.searchstate)
    csp.domain_filter()
    for key in astar.searchstate.domains.keys():
        print key, astar.searchstate.domains[key]
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
    for list_element in copy.deepcopy(permutations):
        for i in range(len(list_element)-1):
            if isinstance(list_element, tuple):
                if not list_element[i] + segments[i]  < list_element[i+1]:
                    #problem here.  Does not remove well enoguh
                    if list_element in permutations:
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
            csp.domains[var] = []
            for i in domain_permutations:
                if i not in csp.domains[var]:
                    csp.domains[var].append(i)

        for column in range(columns):
            segments = [int(x) for x in f.readline().strip().split(' ')]
            segment_domains = generate_segment_domains(segments, rows)
            permutations = calculate_permutations(segment_domains, segments)
            domain_permutations = [create_true_false_array(x, segments, rows) for x in permutations]

            var = Variable(column, "column", row)
            csp.colvars.append(var)
            csp.variables.append(var)
            csp.domains[var] = []
            for i in domain_permutations:
                if i not in csp.domains[var]:
                    csp.domains[var].append(i)



        f.close()
        return csp



if __name__ == "__main__":
    main()

