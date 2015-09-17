__author__ = 'sondredyvik'
class State():
    def __init__(self,xpos,ypos,board):
        self.dimensions = board.dimensions
        self.xpos = xpos
        self.ypos = ypos
        self.parent = None
        self.g = float('inf')
        return

    def __repr__(self):
        return self.type
    def reparent(self, parent):
        self.parent = parent
        self.g = self.parent.g +1
    def calculateHeuristic(self,goalnode):
        self.h = abs(self.xpos - goalnode.xpos)+ abs (self.ypos - goalnode.ypos)
    def calculateNeighbours(self):
        return


