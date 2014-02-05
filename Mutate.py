import numpy as np
from random import randint

# A class to carry out mutations on the alignment
class Mutate():
    smart_dir_prob = 0.5
    """
        Provide matation operators
    """
    def __init__(self, alignment,seq_length,  num_gaps = 1, smart_retry = 3):
        self.alignment = alignment     # an np array holding the alignment
        self.num_gaps = num_gaps       # the number of gaps to insert in gap_insertion()
        self.smart_retry = smart_retry # number of retrys used in smart operators
        self.seq_length = seq_length
        #self.choose_oper()
    
    def __insert_gap(self, row, col):
        """
           take care of inserting a gap in an alignment
           at position row, col
        """
        # make a copy of the rest of the row droping the last '-'
        rest_of_col = self.alignment[row][col:-1].copy()
        #insert a gap '-'
        self.alignment[row][col] = '-'
        # put the rest of the row back after the gap '-'
        self.alignment[row][col+1:] = rest_of_col


    def __close_gap(self, row, col):
        """
           Remove a gap from position row, col 
        """
        # copy all the data after the gap
        row_after_gap = self.alignment[row][col+1:].copy()
        #place that data in the row starting where the gap was
        self.alignment[row][col:-1] = row_after_gap
        #insert the gap at the end of the row
        self.alignment[row][-1] = '-'

    def chooseOper(self):
        """
            randomly choose which if any operator is used on the alignment 
        """
        # First try a even odd for the mutation
        rand_num = randint(1,7)
        if rand_num == 1:
            self.gap_insertion()
        elif rand_num == 2:
            self.gap_shift()
        elif rand_num == 3:
            self.gap_merge()
        elif rand_num == 4:
            self.smart_gap_insertion()
        elif rand_num == 5:
            self.smart_gap_shift()
        elif rand_num == 6:
            self.smart_gap_merge()
        elif rand_num == 7:
            # no mutation
            pass
        
    def gap_insertion(self,num_gaps = 1):
        """
           insert num_gaps number of gaps at a random possition
           in each row
        """
        for i, line in enumerate(self.alignment):
            for j in range(num_gaps):
                position = randint(0,self.seq_length)
                self.__insert_gap(i, position)
        return self.alignment

    def gap_shift(self, all_lines = False):
        """
           randomly choose a gap and move it to another position
           ?? Do we do this on every line
              Or just one randomly chosen
        """
        #count the number of gaps in a row 
        # choose one of them at random and
        # move it to a random place
        rows = []
        if all_lines:
            # all lines is true move a random gap on each line
            for i, line in enumerate(self.alignment):
                rows.append(i)
        else:
            # choose one row at random
            rows.append(randint(0, len(self.alignment)-1))
        
        for row in rows:
            #count the gaps on the row
            num_of_gaps = 0
            for value in self.alignment[row]:
                if value == '-':
                    num_of_gaps += 1
            # randomly choose one of the gaps
            gap_to_move = randint(0,num_of_gaps)
            #find index of gap to move
            gap_count = 0
            gap_index = 0
            for i, value in enumerate(self.alignment[row]):
                #count the gaps to find our randomly choosen gap
                if value == '-':
                    gap_count += 1
                    # we have found the correct gap
                    # save its index and exit the loop 
                    if gap_count == gap_to_move:
                        gap_index = i
                        break

            #close the gap 
            self.__close_gap(row,gap_index)
            print "Removing gap at", row, gap_index
            #choose a random position and insert a gap
            new_gap = randint(0, self.seq_length-1)
            print "Inserting gap at", row, new_gap
            self.__insert_gap(row, new_gap)
        return self.alignment

    def gap_merge(self):
        """
           Select 2 or 3 gaps at random and merge them into one consective
           gap. then move them to a random position
        """
    def smart_gap_insertion(self):
        pass
    def smart_gap_shift(self):
        pass
    def smart_gap_merge(self):
        pass
    def gap_col_remover(self):
        pass
