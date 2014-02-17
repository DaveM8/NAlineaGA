import Mutate
import Scoring
import numpy as np


class Alignment():
    def __init__(self, np_alignment, names, length):
        """Set up the object to pre form an aligment"""
        global scoring_matrix
        self.np_alignment = np_alignment
        self.names = names
        self.length = length
    def fittness(self):
        """Calulate the fittness of an Alignment
           Return a tupel containing (sum-of-pairs, index)
        """
        score = Scoring.Scoring(self.np_alignment, self.length)
        self.score_of_pairs = score.sum_of_pairs()
        self.score_identity = score.identity()
        return self.score_of_pairs, self.score_identity
    def mutation(self):
        """ preform one of the six mutations at random 
            on the aligment. by pasing the data to a
            mutation object
        """
        mu = Mutate.Mutate(self.np_alignment, self.length)
        self.np_alinment = mu.gap_merge()
        #print self.fittness()

    def remove_gap_col(self):
        """
           remove all columns containing only gaps
           there will be 2 types of gap columns 
           ones in between two data containing cols
           ones at the end 
        """
