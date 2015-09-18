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
        self.closedlist=[]
        self.openset = set()
        self.closedset = set()
        #first node is created
        self.searchstate = self.board.generateInitialState()
        #g is set to zero
        self.searchstate.g = 0
        #the searchnodes heuristic is calculated
        self.searchstate.updatef
        #separate methods used to append to openlist.
        self.appendtoopen(self.searchstate,self.type)
        #Extra structure to see make it faster to check if node in openlist
        self.openset.add(self.searchstate)
        #While we have not arrived at the goal

    #Have to implement this method because gui is main loop
    def do_one_step(self):
        #if openlist is empty, no solution is found, return false
        if len(self.openlist) ==0 :
            return False
        #pop element with highest F from openlist
        self.searchstate = self.popfromopen(self.type)
        #remove from support structure
        self.openset.remove(self.searchstate)
        #add to closedlist this node is now about to be expanded
        self.closedlist.append(self.searchstate)
        #add to support structure
        self.closedset.add(self.searchstate)
        #Generate children, these children now get searchstate as parent
        self.searchstate.children = self.searchstate.calculateNeighbours()
        #for each child
        for succ in self.searchstate.children:
            #if child in openset, it has already been created
            if succ in self.openset:
                succ = self.popfromopen(self.type)
                self.openset.remove(succ)
                if self.searchstate.g < succ.parent.g:
                    succ.parent = self
                    succ.calculateHeuristic()
            if succ in self.closedset:
                self.closedlist.remove(succ)
                if self.searchstate.g < succ.parent.g:
                    succ.propagatepathimprovements(self)
                self.closedset.add(succ)
            else:
                self.appendtoopen(succ,self.type)
                self.openset.add(succ)
        if self.searchstate.h ==0:
            return True









    def attach_and_eval(self,child,parent):
        child.parent = parent
        child.g = parent.g +1
        child.updatef()

    def propagate_path_improvement(self, parent):
        for child in parent.children:
            if parent.g +1  < child.g:
                child.parent = parent
                child.g = parent.g+1
                child.updatef()
                self.propagate_path_improvement(child)

    #method to pop from openlist type decides datastructure
    def popfromopen(self,type):
        if self.type =="astar":
            return heappop(self.openlist)
    #method to append to openlist type decides datastructure
    def appendtoopen(self,state,type):
        if self.type =="astar":
            heappush(self.openlist,state)

astar = Astar()
while True:
    astar.do_one_step()