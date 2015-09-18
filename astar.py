__author__ = 'sondredyvik'
import board
import state
from heapq import heappush
from heapq import heappop

class Astar:
    def __init__(self):
        self.board = board.Board('board1.txt')
        self.type ="astar"
        self.openlist =[]
        self.closedset = set()
        self.searchstate = self.board.generateInitialState()
        self.searchstate.g = 0
        self.searchstate.calculateHeuristic()
        self.appendtoopen(self.searchstate,self.type)

        while(not self.searchstate.h ==0):
            if len(self.openlist) ==0:
                return False
            self.searchstate = self.popfromopen()
            self.closedset.add(self.searchstate)
            successors = self.searchstate.calculateNeighbours
            for succ in successors:
                if succ in self.closedset:
                    print "poop"










    def popfromopen(self,type):
        if self.type =="astar":
            return heappop(self.openlist)
    def appendtoopen(self,state,type):
        if self.type =="astar":
            heappush(self.open,(state.f,state))