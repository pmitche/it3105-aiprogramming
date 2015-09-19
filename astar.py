__author__ = 'sondredyvik'
import board
import state
from heapq import heappush, heappop

class Astar:
    def __init__(self):
        #creates an instance of the board class
        self.board = board.Board('board6.txt')
        #variable used to determined search function
        self.type ="astar"
        self.hashtable = {}
        self.openlist =[]
        self.closedlist=[]
        self.opendict = dict()
        self.closeddict = dict()
        #first node is created
        self.searchstate = self.board.generateInitialState()
       # self.searchstate = state.State(11,8,self.board,None)
        #print self.searchstate.calculateNeighbours()

        #g is set to zero
        self.searchstate.g = 0
        #the searchnodes heuristic is calculated
        self.searchstate.updatef()
        #separate methods used to append to openlist.
        self.appendtoopen(self.searchstate,self.type)
        #Extra structure to see make it faster to check if node in openlist
        self.opendict[hash(self.searchstate)] = self.searchstate
        #While we have not arrived at the goal

    #Have to implement this method because gui is main loop
    def do_one_step(self):
        #if openlist is empty, no solution is found, return false
        if len(self.openlist) ==0:
            print "failed"
            for i in range(20):
                for j in range(20):
                    key = hash(str(i)+" "+str(j))
                    if key in self.hashtable:
                        self.hashtable[key] +=1
                        print i,j, self.hashtable[key]
                    else:
                        self.hashtable[key] =1
            print self.hashtable.values()
            return False


        #pop element with highest F from openlist
        self.searchstate = self.popfromopen(self.type)

        #remove from support structure
        del self.opendict[hash(self.searchstate)]
        if self.searchstate.h ==0:
            path = self.findpath(self.searchstate)
            for key in self.opendict:
                self.board.grid[self.opendict[key].xpos][self.opendict[key].ypos] = "O"
            for key in self.closeddict:
                self.board.grid[self.closeddict[key].xpos][self.closeddict[key].ypos] = "C"
            for element in path:
               self.board.grid[element.xpos][element.ypos] = 'X'
            for line in self.board.grid:
                print line
            print "---------------------------------------------------------------------------------------------------------"
            return True


        #add to closedlist this node is now about to be expanded
        self.closedlist.append(self.searchstate)
        #add to support structure
        self.closeddict[hash(self.searchstate)] = self.searchstate
        #Generate children, these children now get searchstate as parent
        successors = self.searchstate.calculateNeighbours()
        #for each child
        for succ in successors:
            if hash(succ) in self.opendict:
                succ = self.opendict[hash(succ)]
            if hash(succ) in self.closeddict:
                succ = self.closeddict[hash(succ)]
            self.searchstate.children.append(succ)
            if hash(succ) not in self.opendict and hash(succ) not in self.closeddict:
                self.attach_and_eval(succ,self.searchstate)
                self.opendict[hash(succ)] = succ
                self.appendtoopen(succ,self.type)
            elif self.searchstate.g + 1 < succ.g:
                self.attach_and_eval(succ,self.searchstate)
                if hash(succ) in self.closeddict:
                    self.propagate_path_improvement(self.closeddict[hash(succ)])








    def findpath(self,state):
        path =[state]
        while state.parent is not None:
            state = state.parent
            path.append(state)
        path.reverse()
        return path




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
done = None
while ( done == None ):
    done = astar.do_one_step()


