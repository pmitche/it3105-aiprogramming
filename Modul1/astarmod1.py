__author__ = 'sondredyvik'
from common import astar
from collections import deque
from heapq import heappush, heappop


class Astarmod1(astar.Astar):
    def __init__(self, type, boardobject):
        self.type = type
        self.board = boardobject
        super(Astarmod1, self).__init__()

    def do_one_step(self):
        # if openlist is empty, no solution is found, return false
        if len(self.openlist) == 0:
            return False


        # pop element with highest F from openlist
        self.searchstate = self.popfromopen()

        #remove from support structure
        del self.opendict[hash(self.searchstate)]
        if self.searchstate.h == 0:
            self.openlist = []
            length = 0
            for state in self.findpath(self.searchstate):
                length += self.arc_cost(state,state.parent)
            print "total length of path: " + str(length-1)
            print self.nodes_created
            return self.findpath(self.searchstate)

        self.closeddict[hash(self.searchstate)] = self.searchstate
        #Generate children, these children now get searchstate as parent
        successors = self.searchstate.calculate_neighbours()
        #for each child
        for succ in successors:
            self.nodes_created +=1
            if hash(succ) in self.opendict:
                succ = self.opendict[hash(succ)]
            if hash(succ) in self.closeddict:
                succ = self.closeddict[hash(succ)]
            self.searchstate.children.append(succ)
            if hash(succ) not in self.opendict and hash(succ) not in self.closeddict:
                self.attach_and_eval(succ, self.searchstate)
                self.opendict[hash(succ)] = succ
                self.appendtoopen(succ)
            elif self.searchstate.g + self.arc_cost(succ, self.searchstate)< succ.g:
                self.attach_and_eval(succ, self.searchstate)
                if hash(succ) in self.closeddict:
                    self.propagate_path_improvement(self.closeddict[hash(succ)])
        return self.findpath(self.searchstate)

    def arc_cost(self, child, parent):
        return 1


    # appends to open in a different matter for each algorithm
    def appendtoopen(self, state):
        if self.type == "astar":
            heappush(self.openlist, state)
        if self.type == "bfs":
            self.openlist.append(state)
        if self.type == "dfs":
            self.openlist.append(state)
     # pops from open in a different matter for each algorithm
    def popfromopen(self):
        if self.type == "astar":
            return heappop(self.openlist)
        if self.type == "bfs":
            return self.openlist.popleft()
        if self.type == "dfs":
            return self.openlist.pop()


    #forwards call to generate initial searchstate
    def generate_initial_searchstate(self):
        return self.board.generateInitialState()
    #Generates openlist
    def generate_openlist(self):
        if self.type == "bfs":
            openlist = deque()
        else:
            openlist = []
        return openlist