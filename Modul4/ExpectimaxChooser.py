__author__ = 'sondredyvik'


import pathos.multiprocessing as mp
from copy import deepcopy
from random import randint
from state import State

TopLeftGrading = [
    [1000,500,300,200],
    [500,400,0,0],
    [300,0,0,0],
    [200,0,0,0]
]
TopRightGrading = [
    [200,300,500,1000],
    [0,0,400,500],
    [0,0,0,300],
    [0,0,0,200]]
BottOmLeftGrading = [
    [200,0,0,0],
    [300,0,0,0],
    [500,400,0,0],
    [1000,500,300,200]]
BottomRightGrading = [
    [0,0,0,200],
    [0,0,0,300],
    [0,0,400,500],
    [200,300,500,1000]]

pool = mp.Pool(4)
class ExpectimaxChooser:
    def __init__(self,board):
        self.board = board
        self.directions =["up","down","left","right"]


    def process_for_pool(self,args):
        return (args[0],self.expectimax(args[1],args[2]))

    def recommend_move(self,node,depth,multiprocessing):

        tuples = []
        if not multiprocessing:
            choices = []
        up = State(deepcopy(node.board),deepcopy(node.score))
        down = State(deepcopy(node.board),deepcopy(node.score))
        left = State(deepcopy(node.board),deepcopy(node.score))
        right = State(deepcopy(node.board),deepcopy(node.score))
        if self.board.move("up",up):
            if multiprocessing:
                tuples.append(("up",up,depth))
            if not multiprocessing:
                choices.append (("up",self.expectimax(up,depth)))
        if self.board.move("down",down):
            if multiprocessing:
                tuples.append(("down",down,depth))
            if not multiprocessing:
                choices.append (("down",self.expectimax(down,depth)))
        if self.board.move("left",left):
            if multiprocessing:
                tuples.append(("left",left,depth))
            if not multiprocessing:
                choices.append (("left",self.expectimax(left,depth)))
        if self.board.move("right",right):
            if multiprocessing:
                tuples.append(("right",right,depth))
            if not multiprocessing:
                choices.append (("right",self.expectimax(right,depth)))

        if multiprocessing:
            pool = mp.Pool(4)
            choices = pool.map(self.process_for_pool, tuples)


        if choices:
            best_choice = choices[0]
            for choice in choices:
                if choice[1] > best_choice[1]:
                    best_choice = choice
            return best_choice[0]




        # choices = []
        # up = State(deepcopy(node.board),deepcopy(node.score))
        # if self.board.move("up", up):
        #     choices.append(("up",self.expectimax(up, depth)))
        #
        # down = State(deepcopy(node.board),deepcopy(node.score))
        # if self.board.move("down", down):
        #      choices.append(("down",self.expectimax(down, depth)))
        #
        # left = State(deepcopy(node.board),deepcopy(node.score))
        # if self.board.move("left", left):
        #     choices.append(("left",self.expectimax(left, depth)))
        #
        # right = State(deepcopy(node.board),deepcopy(node.score))
        # if self.board.move("right", right):
        #     choices.append(("right",self.expectimax(right, depth)))
        # #
        # if choices:
        #     best_choice = choices[0]
        #     for choice in choices:
        #         if choice[1] > best_choice[1]:
        #             best_choice = choice
        #     return best_choice[0]


    def expectimax(self, node, depth):
        if depth == 0:
            return self.calculate_heuristic(node)
        elif depth % 2 == 0:
            value = float("-inf")
            for child in self.create_children(node):
                value = max(value, self.expectimax(child,depth-1))
        elif depth % 2 ==1:
            value = 0
            for child in self.create_children_for_random_node(node):
                value = value +(child[0]*self.expectimax(child[1],depth-1))

        return value




    def calculate_heuristic(self,node):
        return node.score
        # TopLeftPoints = 0
        # TopRightPoints = 0
        # BottomLeftPoints = 0
        # BottomRightPoints = 0
        # for i in range(4):
        #     for j in range(4):
        #         TopLeftPoints += node.board[i][j]*TopLeftGrading[i][j]
        #         TopRightPoints += node.board[i][j]*TopRightGrading[i][j]
        #         BottomLeftPoints += node.board[i][j]*BottOmLeftGrading[i][j]
        #         BottomRightPoints += node.board[i][j]*BottomRightGrading[i][j]
        #
        # returnval = max (TopLeftPoints,TopRightPoints,BottomLeftPoints,BottomRightPoints)
        #
        #
        # for i in self.board.get_free_positions(node):
        #    returnval += 0.05*returnval
        # return returnval

    def create_children_for_random_node(self, node):
        node_children = []
        free_slots = self.board.get_free_cells(node)
        for slot in free_slots:
            new_node = State(deepcopy(node.board),deepcopy(node.score))
            n = randint(1,10)
            if n >9:
                tile = 4
                p =0.1
            else:
                tile = 2
                p = 0.9
            new_node.board[slot[0]][slot[1]] = tile
            node_children.append((p,new_node))
        return node_children

    def create_children(self, node):
        node_children = []
        child_node = State(deepcopy(node.board),deepcopy(node.score))
        for direction in self.directions:
            if self.board.move(direction, child_node):
                node_children.append(child_node)
                child_node = State(deepcopy(node.board),deepcopy(node.score))
        return node_children



