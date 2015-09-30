__author__ = 'sondredyvik'


class Constraint:
    def __init__(self, vertices):
        self.vertices = vertices

    def __repr__(self):
        return str((self.vertices[0],self.vertices[1]))

    def __eq__(self, other):
        return self.vertices[0] == other.vertices[0] and self.vertices[1] == other.vertices[1]

    def check_if_satisfies(self, focal, other):
        return not focal == other

    def contains_variable(self, variable):
        return self.vertices[0] == variable or self.vertices[1] == variable

    def get_other(self, var):
        if self.vertices[0] == var:
            return [self.vertices[1]]
        if self.vertices[1] == var:
            return [self.vertices[0]]
        else:
            raise AttributeError