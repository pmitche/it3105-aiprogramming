__author__ = 'sondredyvik'
from common import astar
from collections import deque
from heapq import heappush, heappop


class Astarmod1(astar.Astar):
    def __init__(self, type, boardobject):
        self.type = type
        self.board = boardobject
        super(Astarmod1, self).__init__()



    def arc_cost(self, child, parent):
        return 1
    def generate_successors(self):
        return self.searchstate.calculate_neighbours()

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