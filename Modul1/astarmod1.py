__author__ = 'sondredyvik'
import astar
from collections import deque
from heapq import heappush, heappop


class Astarmod1(astar.Astar):
    def __init__(self, type, boardobject):
        self.type = type
        self.board = boardobject
        super(Astarmod1, self).__init__(boardobject)


    def arc_cost(self, child, parent):
        return 1

    def appendtoopen(self, state):
        if self.type == "astar":
            heappush(self.openlist, state)
        if self.type == "bfs":
            self.openlist.append(state)
        if self.type == "dfs":
            self.openlist.append(state)

    def popfromopen(self):
        if self.type == "astar":
            return heappop(self.openlist)
        if self.type == "bfs":
            return self.openlist.popleft()
        if self.type == "dfs":
            return self.openlist.pop()

    def generate_initial_searchstate(self):
        return self.board.generateInitialState()

    def generate_openlist(self):
        if self.type == "bfs":
            openlist = deque()
        else:
            openlist = []
        return openlist