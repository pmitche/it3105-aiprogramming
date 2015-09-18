import state

class Board():
    def __init__(self,filename):
        inputhandler = InputHandler(filename)
        self.dimensions = inputhandler.getDimensions()
        self.start = inputhandler.getStart()
        self.goal = inputhandler.getGoal()
        self.obstacles = inputhandler.getObstacles()

        self.grid =[[' ' for j in range(int(self.dimensions[0]))]for i in range( int(self.dimensions[1]))]
        self.grid[int(self.goal[0])][int(self.goal[1])] = 'G'
        self.grid[int(self.start[0])][int(self.start[1])] ='S'
        for obs in self.obstacles:
            x = int(obs[0])
            y= int(obs[1])
            width=int(obs[2])
            height =int(obs[3])
            for i in range(x,x+width):
                for j in range (y,y+height):
                    self.grid[i][j] = '#'
        for line in self.grid:
            print line
    def generateInitialState(self):
        for i in range (len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 'G':
                    return state.State(i, j, self)









class InputHandler():
    def __init__(self,filename):
        f = open(filename,'r')
        self.dimens = f.readline().rstrip().translate(None,'()').split(',')
        self.startandgoal = f.readline().rstrip()
        self.start = self.startandgoal.split(')(')[0].strip('()').split(',')
        self.goal =self.startandgoal.split(')(')[1].strip('()').split(',')
        self.obstaclesHack = f.readlines()
        self.obstacles = []
        for line in self.obstaclesHack:
            line = line.rstrip()
            line = line.translate(None,'()')
            self.obstacles.append(line.split(','))


    def getDimensions(self):
        return self.dimens
    def getStart(self):
        return self.start
    def getGoal(self):
        return self.goal
    def getObstacles(self):
        return self.obstacles




