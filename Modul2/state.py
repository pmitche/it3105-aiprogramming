__author__ = 'sondredyvik'


class State():
    def __init__(self, domains):
        self.domains = domains
        self.h = float('inf')
        self.g = float('inf')
        self.children = []
        self.parent = None
        self.f = self.g + self.g

    def __repr__(self):
        return str(self.domains)

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

    def calculate_heuristics(self):
        self.h = 0
        for key in self.domains.keys():
            self.h += len(self.domains[key]) - 1
