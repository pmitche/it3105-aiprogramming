import math

from Modul6 import ann
import theano
import theano.tensor as T
import numpy as np
from Modul6.gui_from_instructor import *
import heapq



class aiwindow(GameWindow):

    def __init__(self,player,control):
        super(aiwindow, self).__init__()
        self.control = control
        self.player = player
        self.movedict ={}
        self.movedict[0] = 'up'
        self.movedict[1] = 'down'
        self.movedict[2] = 'left'
        self.movedict[3] = 'right'

    def onKeyPress(self,direction):
        if self.board.move(direction, self.board.state):
            self.update_view(self.board.state.board)
            self.board.place_tile(self.board.state)
            self.update_view(self.board.state.board)
            return True
        return False


    def play(self):
        directions = list(self.player.net.predict([self.convertBoard()])[0])
        self.playBestMove(directions)

    def playBestMove(self,directions):
        dir = directions
        dir_val_tups=[]
        for i in range(len(directions)):
            dir_val_tups.append((dir[i],i))
        dir_val_tups.sort()
        for elem in dir_val_tups:
            if self.onKeyPress(self.movedict[elem[1]]):
               break

    def convertBoard(self):
        returnboard = []
        for listelem in self.board.board:
            for elem in listelem:
                returnboard.append(elem)
        return np.array(returnboard)
    def restart(self):
        self.control.new_game()


class NNplayer(object):

    def __init__(self):
        self.train_boards= None
        self.train_moves = None
        self.net = ann.ANN(16,[10],[T.nnet.sigmoid],4, 0.05)

    def load_test_cases(self):
        f = open('myfile1.txt','r' )
        boards=[]
        moves =[]
        lines = f.readlines()
        for line in lines:
            case = line.split('$')
            board = case[0]
            move = case[1]
            board = board.split(',')
            move = move.strip('\n').split(',')
            boards.append(board)
            moves.append(move)
        boards = np.asarray(boards, dtype=np.float)
        self.scale(boards)
        moves = np.array(moves)
        self.train_boards = boards
        self.train_moves = moves

    def scale(self, seq):
        """
        Scales a list of board states by first getting the log2 value of every cell,
        and then dividing every cell by the log2 value of the maximum cell in that board state.

        Example:
            Input   = [[0, 2, 4, 8, 2, 16, 256], [4, 8, 512]]
            Log2    = [[0, 1, 2, 3, 1, 4, 8], [2, 3, 9]
            Scaled  = [[0, 0.125, 0.25, 0.375, 0.125, 0.5, 1], [0.222, 0.333, 1]] (by dividing by max(Log2))

        :param seq: A list of board states, formatted as float (important!)
        :return: A scaled list of board states, ranging from 0 to 1
        """
        for i in range(len(seq)):
            for j in range(len(seq[i])):
                if seq[i][j] != 0:
                    seq[i][j] = np.log2(seq[i][j])
            seq[i] = seq[i] / max(seq[i])

    def train_model(self,epochs, minibatch_size):
        for epoch in range(epochs):
            print("Training epoch number {}...".format(epoch))
            cost = 0
            for i in range(0, len(self.train_boards), minibatch_size):
                image_batch = self.train_boards[i:i+minibatch_size]
                label_batch = self.train_moves[i:i+minibatch_size]
                cost += self.net.train(image_batch, label_batch)

            print("Cost after epoch {}: {}".format(epoch, cost/len(self.train_boards)))


    def test_model(self):
        correct =0
        wrong = 0
        for i in range(len(self.train_moves)):
            if(self.net.predict(self.train_boards)[i] == np.argmax(self.train_moves[i])):
                correct += 1
            else:
                wrong +=1
        print (correct)
global root


class main:

    def __init__(self):
        self.player = NNplayer()
        self.player.load_test_cases()
        self.player.train_model(50,5)
        self.root = Tk()
        game = aiwindow(self.player,self)
        game.pack()
        self.root.bind('<Left>', lambda x : game.onKeyPress("left") )
        self.root.bind('<Up>', lambda x : game.onKeyPress("up") )
        self.root.bind('<Right>', lambda x : game.onKeyPress("right"))
        self.root.bind('<Down>', lambda x : game.onKeyPress("down"))
        self.root.bind('<a>', lambda x: game.play())
        self.root.bind('<n>', lambda x: game.restart())
        self.root.mainloop()

    def new_game(self):
        self.root.destroy()
        self.root = Tk()
        game = aiwindow(self.player,self)
        game.pack()
        self.root.bind('<Left>', lambda x : game.onKeyPress("left") )
        self.root.bind('<Up>', lambda x : game.onKeyPress("up") )
        self.root.bind('<Right>', lambda x : game.onKeyPress("right"))
        self.root.bind('<Down>', lambda x : game.onKeyPress("down"))
        self.root.bind('<a>', lambda x: game.play())
        self.root.bind('<n>', lambda x: game.restart())

if __name__ == '__main__':
    main()