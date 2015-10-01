__author__ = 'sondredyvik'
import state as abstractstate

class StateMod1(abstractstate.State):

    def __init__(self, xpos, ypos, board, parent):
        self.board = board
        self.dimensions = board.dimensions
        self.xpos = xpos
        self.ypos = ypos
        super(StateMod1, self).__init__(parent)

    def __repr__(self):
        return str(self.xpos) + " " + str(self.ypos)

    def calculate_heuristic(self):
        self.h = abs(self.xpos - int(self.board.goal[0])) + abs(self.ypos - int(self.board.goal[1]))

    def calculate_neighbours(self):
        board = self.board
        neighbours = []
        x = self.xpos
        y = self.ypos
        if not self.node_out_of_bounds(x - 1, y) and not self.is_wall(x - 1, y):
            neighbours.append(StateMod1(x - 1, y, board, self))

        if not self.node_out_of_bounds(x, y + 1) and not self.is_wall(x, y + 1):
            neighbours.append(StateMod1(x, y + 1, board, self))
        if not self.node_out_of_bounds(x + 1, y) and not self.is_wall(x + 1, y):
            neighbours.append(StateMod1(x + 1, y, board, self))

        if not self.node_out_of_bounds(x, y - 1) and not self.is_wall(x, y - 1):
            neighbours.append(StateMod1(x, y - 1, board, self))

        return neighbours

    def is_wall(self, x, y):
        return self.board.grid[x][y] == '#'

    def node_out_of_bounds(self, x, y):
        if 0 <= x < int(self.board.dimensions[0]) and 0 <= y < int(self.board.dimensions[1]):
            return False
        return True

    def __hash__(self):
        return hash(str(self.xpos) + "," + str(self.ypos))