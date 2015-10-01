__author__ = 'sondredyvik'
import copy

class State(object):
    def __init__(self):
        self.h = float('inf')
        self.g = float('inf')
        self.children = []
        self.parent = None
        self.f = self.h + self.g


    def reparent(self,parent):
        self.parent = parent
        self.update_f()

    def update_f(self):
        self.f = self.g + self.h

    def check_if_contradictory(self):
        raise NotImplementedError


    def check_if_goal_state(self):
        raise NotImplementedError

    def calculate_neighbours(self,csp):

       raise NotImplementedError

    def calculate_heuristics(self):
        raise NotImplementedError

    def __eq__(self, other):
        return self.f == other.f

    def __hash__(self):
        raise NotImplementedError

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