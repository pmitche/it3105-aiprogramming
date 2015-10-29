__author__ = 'sondredyvik'
from heapq import heappop, heappush


class State(object):
    def __init__(self):
        # Initialises the searchstate. It has to know about board to calculate neighbours
        self.h = float('inf')
        self.g = float('inf')
        self.nodes_created = 0
        self.children = []
        self.parent = None
        self.f = self.g + self.h

    # #adds the new parent to the heap of parents. If it is at the top, it has the lowest g value
    def reparent(self, parent):
        self.parent = parent
        self.update_f()

    # Calculates heuristic using manhattan distance

    def calculate_heuristic(self):
        raise NotImplementedError

    # updates f
    def update_f(self):
        self.f = self.h + self.g

    # Returns list of neighbours. Checks all directions. If they are within the grid and not a wall, a new
    # search state is created with self as parent.
    def calculate_neighbours(self):
       raise NotImplementedError

    # Overrided to use in comparisons
    def __eq__(self, other):
        return self.f == other.f

    #Overrided to use in comparisons
    def __lt__(self, other):
        if self == other:
            return self.h < other.h
        return self.f < other.f

    #Overrided to use in comparisons
    def __gt__(self, other):
        if self == other:
            return self.h > other.h
        return self.f > other.f

    def __repr__(self):
        raise NotImplementedError