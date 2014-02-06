import Mutate
import numpy as np

scoring_matrix = None 

class Alignment():
    def __init__(self, np_alignment, names, length):
        """Set up the object to pre form an aligment"""
        global scoring_matrix
        self.np_alignment = np_alignment
        self.names = names
        self.length = length
        self.score_of_pairs = 0
        self.score_identity = 0
        scoring_matrix = self.__read_matrix('PAM350.csv')
    def fittness(self):
        """Calulate the fittness of an Alignment
           Return a tupel containing (sum-of-pairs, index)
        """
        self.score_of_pairs = self.sum_of_pairs()
        self.score_identity = self.identity()
        return self.score_of_pairs, self.score_identity
    def mutation(self):
        """ preform one of the six mutations at random 
            on the aligment. by pasing the data to a
            mutation object
        """
        mu = Mutate.Mutate(self.np_alignment, self.length)
        self.np_alinment = mu.gap_merge()
        #print self.fittness()
    def sum_of_pairs(self):
        """
           calculate the sum-op-pairs of an alignment
           using the PAM 350 Matrix
        """
        global scoring_matrix
        
        #calculate the score of the current alignment
        self.score_of_pairs = 0    # start at 0
        # go through all the rows
        for row_num, line in enumerate(self.np_alignment):
            # and all the remaining rows 
            for other_row in range(row_num+1,len(self.np_alignment[0])-1):
                # stop brfore trying to compare a row that dose not exsits
                if other_row > len(self.np_alignment)-1: break
                 # and each value in a row
                for col_num, value in enumerate(line):
                    # get the two letters we want to compare
                    score_str = self.np_alignment[row_num][col_num] \
                              + self.np_alignment[other_row][col_num]
                    #convert them to upper
                    score_str = score_str.upper()
                    # add (or subtract) the value found for the two protines
                    # to the sum_of_pairs 
                    self.score_of_pairs += int(scoring_matrix[score_str])
        return self.score_of_pairs
                

    def __read_matrix(self, path_to_matrix):
        matrix = []
        matrix_file = open(path_to_matrix)
        
        for line in matrix_file:
            line = line.strip()
            line = line.split(',')
            matrix.append(line)

        # create a dictionaty where the values can be looked up
        matrix_dict = {}
        
        for i, line in enumerate(matrix):
            for j, value in enumerate(matrix):
                key_str = str(matrix[0][i]) + str(matrix[j][0])
                key_str = key_str.strip()
                matrix_dict[key_str] = matrix[i][j]
        return matrix_dict

    def identity(self):
        """
           How many columnes are lined up correctoly
        """
        col_size = len(self.np_alignment[0])
        # check every coloum of the array
        for i in range(len(self.np_alignment)):
            #select a coloum
            col = self.np_alignment[:,i]
            col_set = set(col)
            if len(col_set) == 1:
                # there is only one value in the set the column is equal
                self.score_identity += 1
        return self.score_identity
    def remove_gap_col(self):
        """
           remove all columns containing only gaps
           there will be 2 types of gap columns 
           ones in between two data containing cols
           ones at the end 
        """
