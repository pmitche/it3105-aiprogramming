__author__ = 'paulpm'


class Astar(object):
    def __init__(self):

        # variable used to determined search function
        self.nodes_expanded= 0
        self.nodes_created = 0
        self.closedlist = []
        self.opendict = dict()
        self.closeddict = dict()
        self.openlist = self.generate_openlist()

        # first node is created
        self.searchstate = self.generate_initial_searchstate()
        self.nodes_created +=1

        # self.searchstate = state.State(11,8,self.board,None)
        #print self.searchstate.calculateNeighbours()

        #g is set to zero
        self.searchstate.g = 0
        #the searchnodes heuristic is calculated
        self.searchstate.update_f()
        #separate methods used to append to openlist.
        self.appendtoopen(self.searchstate)
        #Extra structure to see make it faster to check if node in openlist
        self.opendict[hash(self.searchstate)] = self.searchstate
        #While we have not arrived at the goal

    # Have to implement this method because gui is main loop
    def do_one_step(self):
        raise NotImplementedError

    def generate_openlist(self):
        raise NotImplementedError

    def generate_initial_searchstate(self):
        raise NotImplementedError
    def generate_successors(self):
        raise NotImplementedError

    def findpath(self, state):
        path = [state]
        while state.parent is not None:
            state = state.parent
            path.append(state)
        path.reverse()
        return path


    def attach_and_eval(self, child, parent):
        child.parent = parent
        child.g = parent.g + self.arc_cost(child, parent)
        child.update_f()


    def arc_cost(self, child, parent):
        raise NotImplementedError


    def propagate_path_improvement(self, parent):
        for child in parent.children:
            if parent.g + self.arc_cost(parent, child) < child.g:
                child.parent = parent
                child.g = parent.g + self.arc_cost(parent, child)
                child.update_f()
                self.propagate_path_improvement(child)

    # method to pop from openlist type decides datastructure
    def popfromopen(self):
        raise NotImplementedError

    # method to append to openlist type decides datastructure
    def appendtoopen(self, state):
        raise NotImplementedError


done = None