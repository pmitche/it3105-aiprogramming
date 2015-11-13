__author__ = 'paulpm'


class Variable:
    def __init__(self, index, type, size):
        self.size = size
        self.index = index
        self.type = type

    def __repr__(self):
        return str(self.type)+ str(self.index)

    def __eq__(self, other):
        return self.size == other.size and self.index == other.index and self.type == other.type

    def __hash__(self):
        return hash(str(self.type)+ str(self.index))