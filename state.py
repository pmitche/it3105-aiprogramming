__author__ = 'sondredyvik'
class State():
    def __init__(self,xpos,ypos,board,parent):
        self.dimensions = board.dimensions
        self.xpos = xpos
        self.ypos = ypos
        self.h = float('inf')
        self.parents = []
        self.g = float('inf')
        self.calculateHeuristic(board)
        self. f = self.g + self.h
        self.children =[]

    def __repr__(self):
        return self.type
    def reparent(self, parent):
        self.parent = parent
        self.g = self.parent.g +1
    def calculateHeuristic(self,board):
        self.h = abs(self.xpos - board.goal[0])+ abs (self.ypos - board.goal[1])
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

    def __eq__(self, other):
        return self.f == other.f
    def __hash__(self):
        return hash(str(self.xpos)+str(self.ypos))
    def __lt__(self, other):
        if self == other:
            return self.h < other
        return self.f < other.f
    def __gt__(self, other):
        if self == other:
            return self.h > other.h
        return self.f> other.f