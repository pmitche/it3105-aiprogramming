from module2.cspstate import CspState
import uuid
import copy

__author__ = 'paulpm'


class NoNoState(CspState):
    def __init__(self, domains):
        super(NoNoState,self).__init__(domains)
        self.id = uuid.uuid4()
        self.bannedkeys =[]

    # This method generates a state based on each possible assumption in the domain with the fewest different
    # possibilities. It then reduces their domains using gac rerun.
    # If the domain is valid, the state is returned.
    def calculate_neighbours(self, csp):
        neighbours = []
        smallest = float('inf')
        smallest_domain_key = None
        for key in self.domains.keys():
            if 1 < len(self.domains[key]) < smallest and isinstance(self.domains[key], list) and key not in \
                    self.bannedkeys:
                smallest = len(self.domains[key])
                smallest_domain_key = key
        if smallest_domain_key is None:
            return []

        for assumption in self.domains[smallest_domain_key]:
            assignment = copy.deepcopy(self.domains)
            assignment[smallest_domain_key] = [assumption]
            kid = NoNoState(assignment)
            csp.rerun(kid, smallest_domain_key)
            legal = True
            kid.calculate_heuristics()
            for key in kid.domains.keys():
                if len(kid.domains[key]) == 0:
                    legal = False
            if legal is True:
                neighbours.append(kid)


        return neighbours

    def __hash__(self):
        return hash(self.id)