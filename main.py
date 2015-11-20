from Modul6 import ann
import theano
import theano.tensor as T
import numpy as np
from Modul6.gui_from_instructor import *
import heapq



class aiwindow(GameWindow):

    def __init__(self):
        super(aiwindow, self).__init__()
        self.player = NNplayer()
        self.player.load_test_cases()

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



class NNplayer(object):

    def __init__(self):
        self.train_boards= None
        self.train_moves = None
        self.net = ann.ANN(16,[10],[T.tanh],4,0.1)

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
                self.net.train(image_bulk,result_bulk)


    def test_model(self):
        correct =0
        wrong = 0
        for i in range(len(self.train_moves)):
            if(self.net.predict(self.train_boards)[i] == np.argmax(self.train_moves[i])):
                correct += 1
            else:
                wrong +=1
        print (correct)




root = Tk()

game = aiwindow()
game.pack()


root.bind('<Left>', lambda x : game.onKeyPress("left") )
root.bind('<Up>', lambda x : game.onKeyPress("up") )
root.bind('<Right>', lambda x : game.onKeyPress("right"))
root.bind('<Down>', lambda x : game.onKeyPress("down"))
root.bind('<a>', lambda x: game.play())
root.bind('<n>', lambda x: game.restart())

root.mainloop()


