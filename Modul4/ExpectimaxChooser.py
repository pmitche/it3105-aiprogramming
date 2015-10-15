__author__ = 'sondredyvik'
from copy import deepcopy
from random import randint
from state import State
#TODO FIX SO THAT ALL FUNCTIONS ARE COMPLIANT WITH NODE.BOARD AND NODE.SCORE

TopLeftGrading = [[1000,500,25,10],
                  [500,100,20,8],
                  [25,15,10,5],
                  [10,8, 6,2]]

class ExpectimaxChooser:
    def __init__(self,board):
        self.board = board
        self.directions =["up","down","left","right"]

    def recommend_move(self,node,depth):
        choices = []
        up = State(deepcopy(node.board),deepcopy(node.score))
        if self.board.move("up", up):
            choices.append(("up",self.expectimax(up, depth)))

        down = State(deepcopy(node.board),deepcopy(node.score))
        if self.board.move("down", down):
            choices.append(("down",self.expectimax(down, depth)))

        left = State(deepcopy(node.board),deepcopy(node.score))
        if self.board.move("left", left):
            choices.append(("left",self.expectimax(left, depth)))

        right = State(deepcopy(node.board),deepcopy(node.score))
        if self.board.move("right", right):
            choices.append(("right",self.expectimax(right, depth)))


        if choices:
            best_choice = choices[0]
            for choice in choices:
                if choice[1] > best_choice[1]:
                    best_choice = choice
            return best_choice[0]


    def expectimax(self, node, depth):
        if depth == 0 or self.terminal_test(node):
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



    def terminal_test(self,node):
        return False

    def calculate_heuristic(self,node):
        points = 0
        for i in range(4):
            for j in range(4):
                points += node.board[i][j]*TopLeftGrading[i][j]
        return points

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
