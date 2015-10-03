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
                end_total = columns + 1
                for k in range(j, len(segments)):
                    end_total -= segments[k] + 1
                segment_end_ranges.append(end_total)

            for k in range(len(segments)):
                s = Segment(id_counter, segments[k], row, -1)
                id_counter += 1
                csp.variables.append(s)
                csp.constraints[s] = []
                csp.domains[s] = [int(x) for x in range(segment_start_ranges[k], segment_end_ranges[k]+1)]

            for k in range(1, len(segments)):
                csp.constraints[csp.variables[id_counter-1]].append(
                    Constraint([csp.variables[id_counter-1], csp.variables[id_counter-2]],
                               str(csp.variables[id_counter-1]) + ">" + str(csp.variables[id_counter-2]) + "+" +
                               str(len(csp.domains[csp.variables[id_counter-2]]))))

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

            for k in range(len(segments)):
                s = Segment(id_counter, segments[k], -1, column)
                id_counter += 1
                csp.variables.append(s)
                csp.constraints[s] = []
                csp.domains[s] = [int(x) for x in range(segment_start_ranges[k], segment_end_ranges[k]+1)]

            for k in range(1, len(segments)):
                csp.constraints[csp.variables[id_counter-1]].append(
                    Constraint([csp.variables[id_counter-1], csp.variables[id_counter-2]],
                               str(csp.variables[id_counter-1]) + ">" + str(csp.variables[id_counter-2]) + "+" +
                               str(len(csp.domains[csp.variables[id_counter-2]]))))


        # TODO: Implement method to calculate initial reduced domain using arithmetic
        # TODO: Populate csp.constraints with constraints on the form segmentA.start + segmentA.size > segmentB.start

        print "CSP variables: " + str(csp.variables)
        print "-------------------------------------------------------------"
        print "CSP constraints: " + str(csp.constraints)
        print "-------------------------------------------------------------"
        print "CSP domains: " + str(csp.domains)


        f.close()
        return csp

if __name__ == "__main__":
    main()

