from Mutate import Mutate
import Scoring
import numpy as np


class Alignment():
    def __init__(self, np_alignment, names, length):
        """Set up the object to pre form an aligment"""
        self.np_alignment = np_alignment
        self.names = names
        self.length = length

    def update_length(self):
        """
           keep the length of the sequence up to date
           set the sequence length to the index of the last letter in the 
           alignment
           this method should be run after mutations and crossovers

        """
  
        min_gaps = len(self.np_alignment[0])
        # count in from the end 
        for i, line in enumerate(self.np_alignment):
            current_len = 0
            for j in range(len(self.np_alignment[i])-1, 0, -1):
                if self.np_alignment[i][j] == '-':
                    current_len += 1
                else:
                    if current_len < min_gaps:
                        min_gaps = current_len
                    break
        
        max_len = len(self.np_alignment[0])-1 - min_gaps
        self.length = max_len

    def print_seq(self):
        """
            print out the sequences as nice strings
        """
        for i, line in enumerate(self.np_alignment):
            #print the name of the sequence and the values of the sequence
            # join all the values from the numpy array into a string
            my_str = ''.join(line)
            new_str = ''
            # print the alignment with a space every 10 chars to improve readibilaty
            for j, char in enumerate(my_str):
                new_str += char 
                if j % 10 == 0 and j != 0:
                    new_str += ' '
            print self.names[i] , new_str

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
        mu = Mutate(self)
        self.np_alignment = mu.gap_insertion()

    def remove_gap_col(self):
        """
           remove all columns containing only gaps
           there will be 2 types of gap columns 
           ones in between two data containing cols
           ones at the end 
        """
