from Modul2.csp import CSP
from Modul2.variable import Variable
from Modul2.constraint import Constraint

__author__ = 'paulpm'


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


def main():
    create_csp("nono-cat.txt")


def create_csp(nonogram_file):
        csp = CSP()
        f = open("nonograms/" + nonogram_file, 'r')
        columns, rows = [int(x) for x in f.readline().strip().split(' ')]
        id_counter = 0

        for row in range(rows):
            for size in f.readline().strip().split(' '):
                segment = Segment(id_counter, int(size), row, -1)
                id_counter += 1
                csp.variables.append(segment)
                csp.constraints[segment] = []
                csp.domains[segment] = [int(x) for x in range(rows)]


        for column in range(columns):
            for size in f.readline().strip().split(' '):
                segment = Segment(id_counter, int(size), -1, column)
                id_counter += 1
                csp.variables.append(segment)
                csp.constraints[segment] = []
                csp.domains[segment] = [int(x) for x in range(columns)]


        # TODO: Implement method to calculate initial reduced domain using arithmetic
        # TODO: Populate csp.constraints with constraints on the form segmentA.start + segmentA.size > segmentB.start

        print "CSP variables: " + str(csp.variables)
        print "-------------------------------------------------------------"
        print "CSP constraints: " + str(csp.constraints)
        print "-------------------------------------------------------------"
        print "CSP domains: " + str(csp.domains)










        """for i in range(number_of_vertices):
            index, x, y = [i for i in f.readline().strip().split(' ')]
            vertex = Variable(int(index), float(x), float(y))
            csp.variables.append(vertex)
            csp.constraints[vertex] = []

        for j in range(number_of_edges):
            i1, i2 = [int(i) for i in f.readline().strip().split(' ')]
            this_vertex = csp.variables[i1]
            other_vertex = csp.variables[i2]
            csp.constraints[this_vertex].append(Constraint([this_vertex, other_vertex]))
            csp.constraints[other_vertex].append(Constraint([other_vertex, this_vertex]))

        for k in csp.variables:
            csp.domains[k] = [self.colors[x] for x in range(domain_size)]"""

        f.close()
        #return csp

if __name__ == "__main__":
    main()

