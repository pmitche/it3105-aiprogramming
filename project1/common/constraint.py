__author__ = 'sondredyvik'


class Constraint(object):
    def __init__(self, vertices,expr):
        self.vertices = vertices
        self.expr = expr
        self.function = self.makefunc(["x","y"], self.expr)


    def __repr__(self):
        return str((self.vertices[0],self.vertices[1]))

    def __eq__(self, other):
        return self.vertices[0] == other.vertices[0] and self.vertices[1] == other.vertices[1]

    def makefunc(self, var_names, expression, envir=globals()):
        args = ",".join(var_names)
        return eval("(lambda " + args + ":" + expression + ")", envir)

    def contains_variable(self, variable):
        return variable in self.vertices

    def get_other(self, var):

        if self.vertices[0] == var:
            return [self.vertices[1]]
        if self.vertices[1] == var:
            return [self.vertices[0]]
        else:
            raise AttributeError