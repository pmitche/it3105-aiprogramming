__author__ = 'sondredyvik'

from heapq import heappush, heappop
from common import astar

class Astarmod2(astar.Astar):

    def __init__(self, csp):
        self.csp = csp
        super(Astarmod2, self).__init__()


    def do_one_step(self):
        # if openlist is empty, no solution is found, return false
        if len(self.openlist) == 0:
            return False


        # pop element with highest F from openlist
        self.searchstate = self.popfromopen()
        self.nodes_expanded +=1

        #remove from support structure
        del self.opendict[hash(self.searchstate)]
        if self.searchstate.h == 0:
            self.openlist = []
            return self.findpath(self.searchstate)

        #add to closedlist this node is now about to be expanded
        self.closedlist.append(self.searchstate)
        #add to support structure
        self.closeddict[hash(self.searchstate)] = self.searchstate

        #Generate children, these children now get searchstate as parent
        successors = self.generate_successors()
        #for each child
        for succ in successors:

            if hash(succ) in self.opendict:
                succ = self.opendict[hash(succ)]
            if hash(succ) in self.closeddict:
                succ = self.closeddict[hash(succ)]
            self.searchstate.children.append(succ)
            if hash(succ) not in self.opendict and hash(succ) not in self.closeddict:
                self.nodes_created +=1
                self.attach_and_eval(succ, self.searchstate)
                self.opendict[hash(succ)] = succ
                self.appendtoopen(succ)
            elif self.searchstate.g + 1 < succ.g:
                self.attach_and_eval(succ, self.searchstate)
                if hash(succ) in self.closeddict:
                    self.propagate_path_improvement(self.closeddict[hash(succ)])
        return self.findpath(self.searchstate)

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
