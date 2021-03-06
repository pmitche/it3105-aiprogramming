__author__ = 'sondredyvik'
from common import state
import copy


class CspState(state.State):

    def __init__(self, domains):
        self.domains = domains
        super(CspState, self).__init__()

    #If the domain of any variable is zero, it is a contradictory state
    def check_if_contradictory(self):
        for key in self.domains.keys():
            if len(self.domains[key]) == 0:
                return True
        return False
    #If all domains have length one, we have a goal state.
    def check_if_goal_state(self):
        for key in self.domains.keys():
            if not len(self.domains[key]) == 1:
                return False
        return True

    # This method generates a state based on each possible assumption in the domain with the fewest different
    # possibilities. It then reduces their domains using gac rerun.
    # If the domain is valid, the state is returned.
    def calculate_neighbours(self, csp):
        neighbours = []
        smallest = float('inf')
        smallest_domain_key = None
        for key in self.domains.keys():
            if 1 < len(self.domains[key]) < smallest and isinstance(self.domains[key], list):
                smallest = len(self.domains[key])
                smallest_domain_key = key

        for assumption in self.domains[smallest_domain_key]:
            assignment = copy.deepcopy(self.domains)
            assignment[smallest_domain_key] = [assumption]
            kid = CspState(assignment)
            csp.rerun(kid, smallest_domain_key)
            legal = True
            kid.calculate_heuristics()
            for key in kid.domains.keys():
                if len(kid.domains[key]) == 0:
                    legal = False

            if legal is True:
                neighbours.append(kid)
        self.nodes_created += len(neighbours)
        return neighbours

    #The heuristics here is the length of all (domains -1).
    def calculate_heuristics(self):
        self.h = 0
        for key in self.domains.keys():
            self.h += len(self.domains[key]) - 1
            if len(self.domains[key]) == 0:
                self.h = float('inf')

    def __repr__(self):
        return str(self.domains)

    def __hash__(self):
        hashstring = ''
        for key in self.domains.keys():
            for value in self.domains[key]:
                hashstring += str(value)+"."
        return hash(hashstring)
