

class Crossover():
    """ class to carry out crossover on an alignment
        their are 3 crossover operators one is randomly 
        selected and preformed between two parents to
        produce two child alignmets
    """
    def __init__(self, alignment1, alignment2):
        self.parent1 = alignment1
        self.parent2 = alignment2
    def _chooseCrossover(self):
        """
           Choose at random which crossover to preform
        """
        
class Vertical(Crossover):
    def __init__(self, parent1, parent2):
        self.p1 = parent1
        self.p2 = parent2
        self.preform()
    def preform(self):
        """Do a vertical crossover on between the two parent alignments
           
        """
        pass
class Horizontal(Crossover):
    def __init__(self, parent1, parent2):
        self.p1 = parent1
        self.p2 = parent2
        self.preform()
    def preform(self):
        """Select a line at random and put the top of parent1 with the bottom of parent2
           And the bottom of perent2 with the top of parent1
        """
        pass
class MatchedCol(Crossover):
    def __init__(self, parent1, parent2):
        self.p1 = parent1
        self.p2 = parent2
    def matchedCol(self):
        """Select a fully mached coloum from parent one 
           Select a different fully matched colum from parent2
           add or remove gaps in parent 1 to line up the same 
           column as parent2 with out unalingning the alinged coloum of perent1
        """
        pass
