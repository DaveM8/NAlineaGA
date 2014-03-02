import numpy as np

scoring_matrix = {}
class Scoring():
    def __init__(self, alignment):
        global scoring_matrix
        self.np_alignment = alignment.np_alignment
        self.seq_length = alignment.length
        self.score_of_pairs = 0
        self.score_identity = 0
        if scoring_matrix == {}:
            # only create the global varibal scoring_matrix once
            scoring_matrix = self.__read_matrix('PAM350.csv')
    
    def sum_of_pairs(self):
        """
           calculate the sum-op-pairs of an alignment
           using the PAM 350 Matrix
        """
        global scoring_matrix
        
        try:
        #calculate the score of the current alignment
            self.score_of_pairs = 0    # start at 0
            # go through all the rows
            for row_num, line in enumerate(self.np_alignment):
                # and all the remaining rows 
                for other_row in range(row_num+1,len(self.np_alignment)-1):
                    # stop brfore trying to compare a row that dose not contain data
                    if other_row > self.seq_length-1: break
                     # and each value in a row
                    for col_num in range(0, self.seq_length):
                        #for col_num, value in enumerate(line):
                        # get the two letters we want to compare
                        score_str = self.np_alignment[row_num][col_num] \
                                  + self.np_alignment[other_row][col_num]
                        #convert them to upper
                        score_str = score_str.upper()
                        if len(score_str) != 2:
                            continue
                        # add (or subtract) the value found for the two protines
                        # to the sum_of_pairs 
                        
                        self.score_of_pairs += int(scoring_matrix[score_str])
                        
            return self.score_of_pairs
        except ValueError:
            print "ValueError"
            print scoring_matrix[score_str]
            print row_num, col_num
            print other_row, col_num


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
        
        # check every coloum of the array
        for i in range(len(self.np_alignment[0])):
            #select a coloum
            col = self.np_alignment[:,i]
            # make a set of the column
            col_set = set(col)
            if len(col_set) == 1 and col[0] != '-': # do not count cols of gaps
                # there is only one value in the set the column is aligned
                self.score_identity += 1
        return self.score_identity
