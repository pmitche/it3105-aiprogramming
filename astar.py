__author__ = 'sondredyvik'
import board
import state
from heapq import heappush, heappop

class Astar:
    def __init__(self):
        #creates an instance of the board class
        self.board = board.Board('board1.txt')
        #variable used to determined search function
        self.type ="astar"

        self.openlist =[]
        self.openset = set()
        self.closedset = set()
        #first node is created
        self.searchstate = self.board.generateInitialState()
        #g is set to zero
        self.searchstate.g = 0
        #the searchnodes heuristic is calculated
        self.searchstate.calculateHeuristic()
        #separate methods used to append to openlist.
        self.appendtoopen(self.searchstate,self.type)
        #Extra structure to see make it faster to check if node in openlist
        self.openset.add(self.searchstate)
        #While we have not arrived at the goal
        while not self.searchstate.h ==0 :
            #if openlist is empty, no solution is found, return false
            if len(self.openlist) ==0 :
                return False
            #pop element with highest F from openlist
            self.searchstate = self.popfromopen()
            #remove from support structure
            self.openset.remove(self.searchstate)
            #add to closedset, this node is now about to be expanded
            self.closedset.add(self.searchstate)
            #Generate children, these children now get searchstate as parent
            self.searchstate.children = self.searchstate.calculateNeighbours
            #for each child
            for succ in self.searchstate.children:
                #if child in openset, it has already been created
                if succ in self.openset:
                    succ = self.popfromopen(self.type)
                    self.openset.remove(succ)

                if succ in self.closedset:
                    x = self.closedset.pop(succ)









    def propagatepathimprovements(self,parent):
        return


    #method to pop from openlist type decides datastructure
    def popfromopen(self,type):
        if self.type =="astar":
            return heappop(self.openlist)
    #method to append to openlist type decides datastructure
    def appendtoopen(self,state,type):
        if self.type =="astar":
            heappush(self.open,(state.f,state))