from Modul6 import ann
import theano
import theano.tensor as T
import numpy as np


class NNplayer(object):

    def __init__(self):
        self.train_boards= None
        self.train_moves = None
        self.net = ann.ANN(16,[10],[T.tanh],4,0.05)

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

        boards = np.array(boards)
        moves = np.array(moves)
        self.train_boards = boards
        self.train_moves = moves

    def train_model(self,epochs, minibatch_size):
        for epoch in range(epochs):
            print("Training epoch number {}...".format(epoch))
            error = 0
            i = 0
            j = minibatch_size
            while j < len(self.train_boards):
                image_bulk = self.train_boards[i:j]
                # Creating a result bulk with only zeros
                result_bulk = self.train_moves[i:j]
                i += minibatch_size
                j += minibatch_size
                self.net.train(image_bulk, result_bulk)


            print("Average error per image in epoch {}: {:.3%}".format(epoch, error / j))
    def test_model(self):
        for i in range(len(self.train_boards)):
            print (self.net.predict(self.train_boards[i]))


player = NNplayer()
player.load_test_cases()
player.train_model(10,100)
for i in range(len(player.train_moves)):
    print (player.net.predict(player.train_boards)[i])