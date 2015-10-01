__author__ = 'sondredyvik'


class Astar(object):
    def __init__(self):
        self.opendict = dict()
        self.closeddict = dict()
        self.openlist = self.generate_openlist()
        self.searchnodes_created = 0

        # first node is created
        self.searchstate = self.generate_initial_searchstate()
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
        # if openlist is empty, no solution is found, return false
        if len(self.openlist) == 0:
            return False


        # pop element with highest F from openlist
        self.searchstate = self.popfromopen()

        #remove from support structure
        del self.opendict[hash(self.searchstate)]
        if self.searchstate.h == 0:
            self.openlist = []
            length = 0
            for state in self.findpath(self.searchstate):
                length += self.arc_cost(state,state.parent)
            print "total length of path: " + str(length-1)
            print self.searchnodes_created
            return self.findpath(self.searchstate)

        self.closeddict[hash(self.searchstate)] = self.searchstate
        #Generate children, these children now get searchstate as parent
        successors = self.searchstate.calculate_neighbours()
        #for each child
        for succ in successors:
            self.searchnodes_created +=1
            if hash(succ) in self.opendict:
                succ = self.opendict[hash(succ)]
            if hash(succ) in self.closeddict:
                succ = self.closeddict[hash(succ)]
            self.searchstate.children.append(succ)
            if hash(succ) not in self.opendict and hash(succ) not in self.closeddict:
                self.attach_and_eval(succ, self.searchstate)
                self.opendict[hash(succ)] = succ
                self.appendtoopen(succ)
            elif self.searchstate.g + self.arc_cost(succ, self.searchstate)< succ.g:
                self.attach_and_eval(succ, self.searchstate)
                if hash(succ) in self.closeddict:
                    self.propagate_path_improvement(self.closeddict[hash(succ)])
        return self.findpath(self.searchstate)

    def generate_openlist(self):
        raise NotImplementedError

    def generate_initial_searchstate(self):
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



