__author__ = 'sondredyvik'


class Variable:

    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y

    def __repr__(self):
        return 'n' + str(self.index)

    def __hash__(self):
        return hash((self.index, self.x, self.y))

    def __eq__(self, other):
        return self.index == other.index
