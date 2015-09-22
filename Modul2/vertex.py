__author__ = 'paulpm'


class Vertex:

    def __init__(self, identity, x, y):
        self.id = identity
        self.x = x
        self.y = y

    def __repr__(self):
        return 'n' + str(self.id)