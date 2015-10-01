__author__ = 'sondredyvik'

from heapq import heappush, heappop
import astar

class Astarmod2(astar.Astar):

    def __init__(self, csp):
        self.csp = csp
        super(Astarmod2, self).__init__()


    def generate_initial_searchstate(self):
        return self.csp.generate_initial_searchstate()

    def generate_successors(self):
        return self.searchstate.calculate_neighbours(self.csp)

    def arc_cost(self, child, parent):
        for key in child.domains.keys():
            if len (child.domains[key] ) ==0:
                return float('inf')
        return 1

    def appendtoopen(self, state):
        heappush(self.openlist, state)

    def popfromopen(self):
        return heappop(self.openlist)

    def generate_openlist(self):
        return []
