__author__ = 'sondredyvik'
import copy

class State():
    def __init__(self, domains):
        self.domains = domains
        self.h = float('inf')
        self.g = float('inf')
        self.children = []
        self.parent = None
        self.f = self.update_f()

    def __repr__(self):
        return str(self.domains)

    def update_f(self):
        self.f = self.g + self.h

    def check_if_contradictory(self):
        for key in self.domains.keys():
            if len(self.domains[key]) == 0:
                return True
        return False

    def check_if_goal_state(self):
        for key in self.domains.keys():
            if not len(self.domains[key]) == 1:
                return False
        return True

    def calculate_neighbours(self,csp):
        neighbours = []
        smallest = float('inf')
        smallestdomainkey = None
        for key in self.domains.keys():
            if len(self.domains[key]) < smallest:
                smallest = len(self.domains[key])
                smallestdomainkey = key
        for possible_variable in self.domains[smallestdomainkey]:
            assumption = copy.deepcopy(self.domains)
            assumption[smallestdomainkey] = possible_variable
            neighbours.append(State(assumption))
        for state in neighbours:
            csp.rerun(state,smallestdomainkey)
        return neighbours




    def calculate_heuristics(self):
        self.h = 0
        for key in self.domains.keys():
            self.h += len(self.domains[key]) - 1


    def __eq__(self, other):
        return self.f == other.f

    #Overrided to so that two nodes with same x y values will be considered the same.
    def __hash__(self):
        hashstring = ''
        for key in self.domains.keys():
            for value in self.domains[key]:
                hashstring+= str(value)+"."
        return hash(hashstring)

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