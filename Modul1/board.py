import state


class Board():
    # This class is used to reason about the board.
    # A board is read from file and converted into a 2d array
    # 'S' is start 'G' is goal '#' is obstacle
    def __init__(self, filename):
        inputhandler = InputHandler(filename)
        self.dimensions = inputhandler.dimens
        self.start = inputhandler.start
        self.goal = inputhandler.goal
        self.obstacles = inputhandler.obstacles
        self.filename = filename

        self.grid = [[' ' for j in range(int(self.dimensions[0]))] for i in range(int(self.dimensions[1]))]
        self.grid[int(self.goal[0])][int(self.goal[1])] = 'G'
        self.grid[int(self.start[0])][int(self.start[1])] = 'S'
        for obs in self.obstacles:
            x = int(obs[0])
            y = int(obs[1])
            width = int(obs[2])
            height = int(obs[3])
            for i in range(x, x + width):
                for j in range(y, y + height):
                    self.grid[i][j] = '#'
        for line in self.grid:
            print line

        print "-------------------------------------------------------------------------------"

    #This method is used to provide the astar class with an initial search state.
    #Iterates through textual representation of board and returns a new node
    #with coordinates of start state


    def generateInitialState(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 'S':
                    return state.State(i, j, self, None)


# This class is a basic class to handle input from filename
# First line read is dimensions of grid
#second line read is start and end coordinates
#all subsequent lines are obstacles

class InputHandler():
    def __init__(self, filename):
        f = open(filename, 'r')
        self.dimens = f.readline().rstrip().translate(None, '()').split(',')
        self.startandgoal = f.readline().rstrip()
        self.start = self.startandgoal.split(')(')[0].strip('()').split(',')
        self.goal = self.startandgoal.split(')(')[1].strip('()').split(',')
        self.obstaclesHack = f.readlines()
        self.obstacles = []
        for line in self.obstaclesHack:
            line = line.rstrip()
            line = line.translate(None, '()')
            self.obstacles.append(line.split(','))




