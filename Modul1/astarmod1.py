__author__ = 'sondredyvik'
import astar


class Astarmod1(astar.Astar):
    def __init__(self, types, boardobject):
        super(Astarmod1,self).__init__(types)
        self.board =boardobject

    def arc_cost(self, child, parent):
        return 1

    def generate_initial_searchstate(self):
        return self.board.generateInitialState()