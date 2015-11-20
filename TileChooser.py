__author__ = 'sondredyvik'

from random import randint

class TileChooser:

    def __init__(self):
        self.tiles = []
        self.four_count = 0
        self.two_count = 0

    def choose_tile(self):
        if self.tiles:
            num = self.tiles[randint(0,len(self.tiles)-1)]
            self.tiles.remove(num)
            if num == 2:
                self.two_count +=1
            else:
                self.four_count +=1
            return num

        else:
            [self.tiles.append(2) for x in range(9)]
            self.tiles.append(4)
            num = self.tiles[randint(0,len(self.tiles)-1)]
            self.tiles.remove(num)
            if num == 2:
                self.two_count +=1
            else:
                self.four_count +=1
            return num


tiles = TileChooser()

