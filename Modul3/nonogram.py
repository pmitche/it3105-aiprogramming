from Modul2.astarmod2 import Astarmod2
from common.constraintnet import ConstraintNet
from variable import Variable
from gacmod3 import mod3GAC
import itertools
import copy

__author__ = 'paulpm'

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


    def create_csp(self, nonogram_file):
            CNET = ConstraintNet()
            csp = mod3GAC(CNET)
            f = open(nonogram_file, 'r')
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


