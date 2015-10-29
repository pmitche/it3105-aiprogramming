from state import State
import random

__author__ = 'sondredyvik, paulpm'


class Board(object):

    def __init__(self):
        self.board = [[0 for _ in xrange(4)] for _ in xrange(4)]
        self.free_tiles = []
        self.full = False
        self.score = 0
        self.state = State(self.board, self.score)

    def get_free_cells(self, state):
        free_tuples = []
        for x in xrange(4):
            for y in xrange(4):
                if state.board[x][y] == 0:
                    free_tuples.append((x, y))
        return free_tuples

    def place_tile(self, state):
        choices = [2, 2, 2, 2, 2, 2, 2, 2, 4]
        value = random.choice(choices)
        free_slots = self.get_free_cells(state)
        if free_slots:
            x, y = random.choice(free_slots)
            state.board[x][y] = value
        else:
            self.full = True

    def move_all_tiles_right(self, state):
        moved = False
        for x in reversed(xrange(4)):
            for y in reversed(xrange(4)):
                if state.board[x][y] != 0:
                    for z in xrange(y, -1, -1):
                        if state.board[x][y] == state.board[x][z] and y != z:
                            state.board[x][y] += state.board[x][z]
                            state.board[x][z] = 0
                            state.score += state.board[x][y]
                            moved = True
                            break
                        if state.board[x][z] != 0 and state.board[x][z] != state.board[x][y]:
                            break

        for x in reversed(xrange(4)):
            for y in reversed(xrange(4)):
                if state.board[x][y] == 0:
                    for z in xrange(y, -1, -1):
                        if state.board[x][z] != 0:
                            state.board[x][y] = state.board[x][z]
                            state.board[x][z] = 0
                            moved = True
                            break
        return moved

    def move_all_tiles_left(self, state):
        moved = False
        for x in xrange(4):
            for y in xrange(4):
                if state.board[x][y] != 0:
                    for z in xrange(y, 4):
                        if state.board[x][y] == state.board[x][z] and y != z:
                            state.board[x][y] += state.board[x][z]
                            state.board[x][z] = 0
                            state.score += state.board[x][y]
                            moved = True
                            break
                        if state.board[x][z] != 0 and state.board[x][z] != state.board[x][y]:
                            break

        for x in xrange(4):
            for y in xrange(4):
                if state.board[x][y] == 0:
                    for z in xrange(y, 4):
                        if state.board[x][z] != 0:
                            state.board[x][y] = state.board[x][z]
                            state.board[x][z] = 0
                            moved = True
                            break
        return moved

    def move_all_tiles_down(self, state):
        moved = False
        for y in reversed(xrange(4)):
            for x in reversed(xrange(4)):
                if state.board[x][y] != 0:
                    for z in xrange(x, -1, -1):
                        if state.board[z][y] != 0 and x != z:
                            if state.board[x][y] == state.board[z][y]:
                                state.board[x][y] += state.board[z][y]
                                state.board[z][y] = 0
                                state.score += state.board[z][y]
                                moved = True
                                break
                            if state.board[z][y] != 0 and state.board[z][y] != state.board[x][y]:
                                break

        for y in reversed(xrange(4)):
            for x in reversed(xrange(4)):
                    if state.board[x][y] == 0:
                        for z in xrange(x, -1, -1):
                            if state.board[z][y] != 0:
                                state.board[x][y] = state.board[z][y]
                                state.board[z][y] = 0
                                moved = True
                                break
        return moved

    def move_all_tiles_up(self, state):

        moved = False
        for y in xrange(4):
            for x in xrange(4):
                if state.board[x][y] != 0:
                    for z in xrange(x, 4):
                        if state.board[z][y] != 0 and not x == z:
                            if state.board[x][y] == state.board[z][y]:
                                state.board[x][y] += state.board[z][y]
                                state.board[z][y] = 0
                                state.score += state.board[x][y]
                                moved = True
                                break
                        if state.board[z][y] != 0 and state.board[z][y] != state.board[x][y]:
                            break
        for y in xrange(4):
            for x in xrange(4):
                if state.board[x][y] == 0:
                    for z in xrange(x, 4):
                        if state.board[z][y] != 0:
                            state.board[x][y] = state.board[z][y]
                            state.board[z][y] = 0
                            moved = True
                            break
        return moved

    def move(self, direction, state):

        moved = False
        move = direction
        if move == "up":
            if self.move_all_tiles_up(state):
                moved = True
        elif move == "down":
            if self.move_all_tiles_down(state):
                moved = True
        elif move == "left":
            if self.move_all_tiles_left(state):
                moved = True
        elif move == "right":
            if self.move_all_tiles_right(state):
                moved = True

        return moved

    def __repr__(self):
        return str([(str(x), '\n') for x in self.board])

    def print_self(self, state):
        for x in state.board:
            print x






