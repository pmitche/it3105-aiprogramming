__author__ = 'sondredyvik'
from heapq import heappop,heappush
class State():
    def __init__(self,xpos,ypos,board,parent):
        #Initialises the searchstate. It has to know about board to calculate neighbours
        self.board = board
        self.dimensions = board.dimensions
        self.xpos = xpos
        self.ypos = ypos
        self.h = float('inf')
        self.parent = parent
        self.g = float('inf')
        self.calculateHeuristic()
        self.f = self.g + self.h
        self.children =[]

    def __repr__(self):
        return str(self.xpos)+" "+str(self.ypos)
    ##adds the new parent to the heap of parents. If it is at the top, it has the lowest g value
    def reparent(self, parent):
        self.parent = parent
        self.updatef()
    #Calculates heuristic using manhattan distance

    def calculateHeuristic(self):
        self.h = abs(self.xpos - int(self.board.goal[0]))+ abs (self.ypos - int(self.board.goal[1]))
    #updates f
    def updatef(self):
        self.calculateHeuristic()
        self.f = self.h + self.g
    #Returns list of neighbours. Checks all directions. If they are within the grid and not a wall, a new
    #search state is created with self as parent.
    def calculateNeighbours(self):
        board = self.board
        neighbours = []
        if self.xpos-1  >=0 and self.ypos+1 < board.dimensions[1] and not board.grid[self.xpos-1][self.ypos+1]=='#':
            neighbours.append(State(self.xpos-1,self.ypos+1,board,self))
        if self.xpos +1 < board.dimensions[0] and self.ypos +1 < board.dimensions[1] and not board.grid[self.xpos+1][self.ypos+1]=='#':
            neighbours.append(State(self.xpos+1,self.ypos+1, board,self))
        if self.xpos +1 < board.dimensions[0] and self.ypos -1 >=0 and not  board.grid[self.xpos+1][self.ypos-1]=='#':
            neighbours.append(State(self.xpos+1,self.ypos-1, board,self))
        if self.xpos -1>= 0 and self.ypos-1 >= 0 and not  board.grid[self.xpos-1][self.ypos-1] == '#':
            neighbours.append(State(self.xpos-1,self.ypos-1, board,self))
        if self.xpos -1 >= 0 and not board.grid[self.xpos-1][self.ypos] == '#':
            neighbours.append(State(self.xpos-1,self.ypos, board,self))
        if self.xpos +1 < board.dimensions[0] and not board.grid[self.xpos+1][self.ypos] == '#':
            neighbours.append(State(self.xpos+1,self.ypos,board,self))
        if self.ypos -1 >= 0 and not board.grid[self.xpos][self.ypos-1] =='#':
            neighbours.append(State(self.xpos,self.ypos-1,board,self))
        if self.ypos +1 < board.dimensions[1] and not board.grid[self.xpos][self.ypos+1] =='#':
            neighbours.append(State(self.xpos,self.ypos+1,board,self))
        return neighbours
    #Overrided to use in comparisons
    def __eq__(self, other):
        return self.f == other.f
    #Overrided to so that two nodes with same x y values will be considered the same.
    def __hash__(self):
        return hash(str(self.xpos)+str(self.ypos))
    #Overrided to use in comparisons
    def __lt__(self, other):
        if self == other:
            return self.h < other.h
        return self.f < other.f
    #Overrided to use in comparisons
    def __gt__(self, other):
        if self == other:
            return self.h > other.h
        return self.f> other.f