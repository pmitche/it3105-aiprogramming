__author__ = 'sondredyvik'
from heapq import heappop,heappush
class State():
    def __init__(self,xpos,ypos,board,parent):
        #Initialises the searchstate. It has to know about board to calculate neighbours
        self.dimensions = board.dimensions
        self.xpos = xpos
        self.ypos = ypos
        self.h = float('inf')
        self.parents = []
        self.g = float('inf')
        self.calculateHeuristic(board)
        self.f = self.g + self.h
        self.children =[]

    def __repr__(self):
        return self.type
    ##adds the new parent to the heap of parents. If it is at the top, it has the lowest g value
    def reparent(self, parent):
        heappush(self.parents,(parent.g,parent))
        self.g = self.parents[0][0]+1
        self.calculateHeuristic()

    #Calculates heuristic using manhattan distance

    def calculateHeuristic(self):
        board = self.board
        self.h = abs(self.xpos - board.goal[0])+ abs (self.ypos - board.goal[1])
        self.updatef()
    #updates f
    def updatef(self):
        self.f = self.h + self.g
    #Returns list of neighbours. Checks all directions. If they are within the grid and not a wall, a new
    #search state is created with self as parent.
    def calculateNeighbours(self,board):
        neighbours = []
        if self.xpos-1  >=0 and self.ypos+1 < board.dimensions[1] and not board[self.xpos-1][self.ypos+1]=='#':
            neighbours.append(State(self.xpos-1,self.ypos+1),board,self)
        if self.xpos +1 < board.dimensions [0] and self.ypos +1 < board.dimensions[1] and not board[self.xpos+1][self.ypos+1]=='#':
            neighbours.append(State(self.xpos+1,self.ypos+1, board,self))
        if self.xpos +1 < board.dimensions[0] and self.ypos -1 >=0 and not board[self.xpos+1][self.ypos-1]=='#':
            neighbours.append(State(self.xpos+1,self.ypos-1, board,self))
        if self.xpos -1>= 0 and self.ypos-1 >= 0 and not board[self.xpos-1][self.ypos-1] == '#':
            neighbours.append(State(self.xpos-1,self.ypos-1, board,self))
        if self.xpos -1 >= 0 and not board[self.xpos-1][self.ypos] == '#':
            neighbours.append(State(self.xpos-1,self.ypos, board,self))
        if self.xpos +1 < board.dimensions[0] and not board[self.xpos+1][self.ypos] == '#':
            neighbours.append(State(self.xpos+1,self.ypos,board,self))
        if self.ypos -1 >= 0 and not board[self.xpos][self.ypos-1] =='#':
            neighbours.append(State(self.xpos,self.ypos-1,board,self))
        if self.ypos +1 < board.dimensions[1] and not board[self.xpos][self.ypos+1] =='#':
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
            return self.h < other
        return self.f < other.f
    #Overrided to use in comparisons
    def __gt__(self, other):
        if self == other:
            return self.h > other.h
        return self.f> other.f