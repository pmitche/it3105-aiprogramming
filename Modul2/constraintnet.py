__author__ = 'sondredyvik'



class ConstraintNet:
    def __init__(self):
        self.constraints = {}

    def add_constraint(self,key,constraint):
        if key in self.constraints:
            self.constraints[key].append(constraint)
        else:
            self.constraints[key] = [constraint]
