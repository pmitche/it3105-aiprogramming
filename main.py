from Modul6.ann import ANN
from Modul6.gui_from_instructor import *

import theano.tensor as T
import numpy as np

import copy
import random
import requests


class AiWindow(GameWindow):

    def __init__(self, player, control):
        super(AiWindow, self).__init__()
        self.control = control
        self.player = player
        self.movedict = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}
        self.weight_matrix = [
            [0, 1, 2, 3],
            [6, 5, 5, 4],
            [7, 9, 12, 15],
            [55, 35, 25, 20]
        ]

    def onKeyPress(self, direction):
        if self.board.move(direction, self.board.state):
            self.update_view(self.board.state.board)
            self.board.place_tile(self.board.state)
            self.update_view(self.board.state.board)
            return True
        return False

    def play(self):
        boolean_var = True
        while boolean_var:
            directions = list(self.player.net.predict([self.convert_board()])[0])
            boolean_var = self.play_best_move(directions)

    def play_best_move(self, directions):
        dir = directions
        dir_val_tups = []
        for i in range(len(directions)):
            dir_val_tups.append((dir[i], i))
        dir_val_tups.sort()
        for elem in dir_val_tups:
            if self.onKeyPress(self.movedict[elem[1]]):
                return True
        self.restart(self.board.get_highest_tile())
        return False

    def play_random(self):
        boolean_var = True
        while boolean_var:
            boolean_var = self.play_random_move()

    def play_random_move(self):
        directions = [0, 1, 2, 3]
        moves = []
        for _ in directions:
            rand = random.randint(0, len(directions)-1)
            moves.append(directions[rand])
        for num in directions:
            if self.onKeyPress(self.movedict[num]):
                return True
        self.restart(self.board.get_highest_tile())
        return False

    def calculate_heuristic(self, node):
        value = 0
        for i in range(len(node.board)):
            for j in range(len(node.board[i])):
                value += self.weight_matrix[i][j]
        return value

    # ConvertBoard for expectimax cases
    def convert_board(self):
        returnboard = []
        boards = []
        for i in range(4):
            boards.append(copy.deepcopy(self.board.state))

        self.board.move('up', boards[0])
        self.board.move('down', boards[1])
        self.board.move('left', boards[2])
        self.board.move('right', boards[3])
        for i in range(4):
            returnboard.append(self.calculate_heuristic(boards[i]))
        return np.array(returnboard)

    #
    # def convertBoard(self):
    #     returnboard = []
    #     for listelem in self.board.board:
    #         for elem in listelem:
    #             returnboard.append(elem)
    #     return np.array(returnboard)

    def restart(self, result):
        self.control.new_game(result)


class NNplayer(object):

    def __init__(self, training_set, topology, lr, epochs, batch_size, activation_functions):
        self.training_set = training_set
        self.topology = topology
        self.lr = lr
        self.epochs = epochs
        self.batch_size = batch_size
        self.activation_functions = activation_functions
        self.train_boards = None
        self.train_moves = None
        # Different number of in nodes because of different test set
        if self.training_set == 1:
            self.input = 16
        else:
            self.input = 4
        self.net = ANN(self.input, self.topology, activation_functions, 4, lr)

    def load_test_cases(self):
        if self.training_set == 1:
            f = open('myfile1.txt', 'r')
        else:
            f = open('myfile3.txt', 'r')
        boards = []
        moves = []
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
        scale(boards)
        moves = np.array(moves)
        self.train_boards = boards
        self.train_moves = moves

    def train_model(self, epochs, minibatch_size):
        for epoch in range(epochs):
            print("Training epoch number {}...".format(epoch))
            cost = 0
            for i in range(0, len(self.train_boards), minibatch_size):
                board_batch = self.train_boards[i:i+minibatch_size]
                move_batch = self.train_moves[i:i+minibatch_size]
                cost += self.net.train(board_batch, move_batch)

            print("Cost after epoch {}: {}".format(epoch, cost/len(self.train_boards)))

    def test_model(self):
        correct = 0
        for i in range(len(self.train_moves)):
            if self.net.predict(self.train_boards)[i] == np.argmax(self.train_moves[i]):
                correct += 1
        print(correct)


class main:

    def __init__(self):
        self.gui_bool = str(input("Gui? y/n: \n"))
        self.training_set = str(input("What training set do you want to use?\n1: 16 dim vector, 2: 4 dim vector: \n"))
        self.hidden = [x for x in map(int, input("Please specify a topology description on the form 40,20,60: ").strip().split(","))]
        self.activations = [activation_map(x) for x in list(map(int, input("Please specify activation functions for each layer on the form 0,2,1: ").strip().split(",")))]
        self.lr = float(input("Specify learning rate: "))
        self.epochs = int(input('How many epochs do you want to train?: '))
        self.minibatch = int(input('What batch size do you want to use?: '))
        self.net_result = []
        self.rand_result = []
        self.count = 1
        self.player = NNplayer(self.training_set, self.hidden, self.lr, self.epochs, self.minibatch, self.activations)
        self.player.load_test_cases()
        self.player.train_model(self.epochs, self.minibatch)
        self.root = Tk()
        print('NNET playing round: ' + str(self.count))
        self.game = AiWindow(self.player, self)
        if self.gui_bool == 'y':
            self.game.pack()
            self.root.bind('<a>', lambda x: self.game.play())
            self.root.mainloop()
        if self.gui_bool == 'n':
            self.game.play()

        self.net_result = []
        self.rand_result = []
        self.count = 1

    def new_game(self, result):
        self.game.pack_forget()
        if self.count < 50:
            self.net_result.append(result)
            print('Highest tile: ' + str(result))
            self.count += 1
            print('NNET playing round: ' + str(self.count))
            self.game = AiWindow(self.player, self)
            if self.gui_bool == 'y':
                self.game.pack()
            self.game.play()

        elif self.count == 50:
            print('Highest tile: ' + str(result))
            self.net_result.append(result)
            self.count += 1
            print('NNET playing round: ' + str(self.count))
            self.game = AiWindow(self.player, self)
            if self.gui_bool == 'y':
                self.game.pack()
            self.game.play_random()

        elif 50 < self.count < 100:
            print('Highest tile: ' + str(result))
            self.rand_result.append(result)
            self.count += 1

            print('Random playing round: ' + str(self.count-50))
            self.game = AiWindow(self.player, self)
            if self.gui_bool == 'y':
                self.game.pack()
            self.game.play_random()

        elif self.count == 100:
            # self.count+=1
            self.rand_result.append(result)
            print(len(self.rand_result))
            print(len(self.net_result))
            print(welch(self.rand_result, self.net_result))


def scale(seq):
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


def activation_map(x):
        return {
            0: T.tanh,
            1: T.nnet.sigmoid,
            2: lambda k: T.switch(k > 0, k, 0),  # Equivalent to T.nnet.relu (rectified linear unit)
            3: T.nnet.softmax,
        }.get(x, T.tanh)  # T.tanh is default if x is not found


def welch(list1, list2):
        params = {"results": str(list1) + " " + str(list2), "raw": "1"}
        resp = requests.post('http://folk.ntnu.no/valerijf/6/', data=params)
        return resp.text

if __name__ == '__main__':
    main()
