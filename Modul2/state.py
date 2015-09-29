__author__ = 'sondredyvik'


class State():
    def __init__(self,domains):
        self.domains = domains
        self.h = float('inf')
        self.g = float('inf')
        self.children =[]
        self.f = self.g + self.g

    def __repr__(self):
        return str(self.domains)

    def calculate_heuristics(self):




