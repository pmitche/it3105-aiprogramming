__author__ = 'sondredyvik'
import astar


class Astarmod1(astar.Astar):
    def __init__(self,types,boardobject):
        super(Astarmod1,self).__init__(types, boardobject)

    def arc_cost(self, child, parent):
        return 1