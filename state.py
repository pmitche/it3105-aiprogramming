__author__ = 'sondredyvik'
class State():
    def __init__(xpos,ypos,board):
       return
    def __repr__(self):
        return self.type
    def reparent(self, parent):
        self.parent = parent
    def calculateHeuristic(self,goalnode):
        self.h = abs(self.xpos - goalnode.xpos)+ abs (self.ypos - goalnode.ypos)
    def calculateNeighbours(self):
        return


