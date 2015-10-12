__author__ = 'sondredyvik'
from TileChooser import TileChooser
from random import randint
import os
class Board():
    def __init__(self):
        self.board = [[0 for x in range(4)]for i in range (4)]
        self.free_tiles = []
        self.tile_chooser = TileChooser()
        self.full = False
        self.score = 0

    def __repr__(self):
        return str([(str(x),"\n") for x in self.board])

    def print_self(self):
        for x in self.board:
            print x

    def get_free_positions(self):
        free_tuples = []
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if self.board[x][y] == 0:
                    free_tuples.append((x,y))
        return free_tuples

    def place_tile(self):
        free_slots = self.get_free_positions()
        if free_slots:
            position_to_place_tile = free_slots[randint(0,len(free_slots)-1)]
            self.board[position_to_place_tile[0]][position_to_place_tile[1]] = self.tile_chooser.choose_tile()

        else:
            self.full = True

    def move_all_tiles_right(self):
        moved = False
        for x in reversed(range(4)):
            for y in reversed(range(4)):
                if self.board[x][y] != 0:
                    for z in range(y,-1,-1):
                        if self.board [x][y] == self.board[x][z] and y !=z:
                            self.board[x][y] += self.board [x][z]
                            self.score += self.board[x][y]
                            self.board[x][z] = 0
                            moved = True
                            break
                        if self.board[x][z] !=0 and self.board[x][z] != self.board[x][y]:
                            break

        for x in reversed(range(4)):
            for y in reversed(range(4)):
                if self.board[x][y] ==0:
                    for z in range(y,-1,-1):
                        if self.board[x][z] !=0:
                            self.board[x][y] = self.board[x][z]
                            self.score += self.board[x][y]
                            self.board[x][z] = 0
                            moved = True
                            break
        return moved

    def move_all_tiles_left(self):
        moved = False
        for x in range(4):
            for y in range(4):
                if self.board[x][y] != 0:
                    for z in range(y,4):
                        if self.board [x][y] == self.board[x][z] and y !=z:
                            self.board[x][y] += self.board [x][z]
                            self.score += self.board[x][y]
                            self.board[x][z] = 0
                            moved = True
                            break
                        if self.board[x][z] !=0 and self.board[x][z] != self.board[x][y]:
                            break

        for x in range(4):
            for y in range(4):
                if self.board[x][y] ==0:
                    for z in range(y,4):
                        if self.board[x][z] !=0:
                            self.board[x][y] = self.board[x][z]
                            self.board[x][z] = 0
                            moved = True
                            break
        return moved

    def move_all_tiles_down(self):
        moved = False
        for y in reversed(range(4)):
            for x in reversed(range(4)):
                if self.board[x][y]!=0:
                    for z in range(x,-1,-1):
                        if self.board[z][y] !=0 and x != z:
                            if self.board[x][y] == self.board[z][y]:
                                self.board[x][y] += self.board[z][y]
                                self.score += self.board[x][y]
                                self.board[z][y] = 0
                                moved = True
                                break
                            if self.board[z][y]!=0 and self.board[z][y]!=self.board[x][y]:
                                break

        for y in reversed(range(4)):
            for x in reversed(range(4)):
                    if self.board[x][y] == 0:
                        for z in range(x,-1,-1):
                            if self.board[z][y] != 0:
                                self.board[x][y] = self.board[z][y]
                                self.board[z][y] = 0
                                moved = True
                                break
        return moved

    def move_all_tiles_up(self):
        moved = False
        for y in range(4):
            for x in range(4):
                if self.board[x][y]!=0:
                    for z in range (x,4):
                        if self.board[z][y] !=0 and not x ==z:
                            if self.board[x][y] == self.board[z][y]:
                                self.board[x][y] += self.board[z][y]
                                self.score += self.board[x][y]
                                self.board[z][y] = 0
                                moved = True
                                break
                        if self.board[z][y] != 0 and self.board[z][y] != self.board[x][y]:
                            break
        for y in range(4):
            for x in range(4):
                if self.board[x][y] ==0:
                    for z in range (x,4):
                        if self.board[z][y] != 0:
                            self.board[x][y] = self.board[z][y]
                            self.board[z][y] = 0
                            moved = True
                            break
        return moved

    def listen_for_move(self):
        print "Score: " + str(self.score)

        self.print_self()
        move = raw_input("Do a move (awsd):\n")
        legal_moves = ["a","d","s","w","q"]
        if move not in legal_moves:
            print "NOT LEGAL"
            return
        else:
            if move == "w":
                if self.move_all_tiles_up():
                    self.place_tile()
                    print "moved up"

            elif move =="s":
                if self.move_all_tiles_down():
                    print "moved down"
                    self.place_tile()
            elif move =="a":
                if self.move_all_tiles_left():
                    print "moved left"
                    self.place_tile()
            elif move =="d":
                if self.move_all_tiles_right():
                    print "moved right"
                    self.place_tile()
            elif move =="q":
                self.full = True





