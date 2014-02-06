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
        #print "Inserting gap at", row, col
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
        #print "Removing gap at", row, col
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
                    # we have found the correct gap
                    # save its index and exit the loop 
                    if gap_count == gap_to_move:
                        gap_index = i
                        break
                    gap_count += 1

            #close the gap 
            self.__close_gap(row,gap_index)
            print "Removing gap at", row, gap_index
            #choose a random position and insert a gap
            new_gap = randint(0, self.seq_length-1)
            print "Inserting gap at", row, new_gap
            self.__insert_gap(row, new_gap)
        return self.alignment

    def gap_merge(self, all_lines = False):
        """
           Select 2 or 3 consective  gaps at random and merge
           them into one consective gap. then move them to a random position
           
           NOTE when removing 2 gaps if the randomly selected gap is the first or last 
           it will be mearged with a gap at the start for the last or the end for last
           
           But when removing 3 gaps the 3 gaps will always be at the same end
           Maybe I'll change this later

           NOTE look into how __insert_gap works to make sure I dont lose letters
           when palcing new gaps 
        """
        # count the gaps 
        # work out how many different 2 and 3 gap patterns
        # there are

        # create a list of all the rows or just one 
        # randomly choosen row
        rows = []
        if all_lines:
            # all lines is true merge and move gaps on all lines
            for i, line in enumerate(self.alignment):
                rows.append(i)
        else:
            # choose one row at random
            rows.append(randint(0, len(self.alignment)-1))
        
        for row in rows:
            # count the number of gaps
            num_of_gaps = 0
            for value in self.alignment[row]:
                if value == '-':
                    num_of_gaps += 1
            # so how many 2 or 3 gap patterns are threre
            two_or_three = randint(2,3)
            #print "two_or_three=", two_or_three
            # choose a gap at random
            # if we want 3 take the gap on each side
            # if we want 2 toss a coin
            
            # randomly choose a gap 
            gap_to_move = randint(0, num_of_gaps-1)
            # find the index of the gap 
            gap_index = self.__find_gap_index(row, gap_to_move)
            #print "gap_to_move =", gap_to_move
            #print "gap_index =", gap_index
            # now I have the index of a random gap and 
            # I know if I want 2 or three gaps
            if two_or_three == 2:
                left_or_right = randint(0,1)
                #print "left_or_right=", left_or_right
                if left_or_right == 0:
                    #look for a gap on the left
                    if gap_to_move == 0:
                        # the gap in the first gap in the sequence
                        # merge it with the last gap in the sequence
                        second_gap_index = self.__find_gap_index(row, num_of_gaps)
                    else:
                        second_gap_index = self.__find_gap_index(row, gap_to_move-1)
                else:
                    # look on the right 
                    if gap_to_move == num_of_gaps:
                        # the gap is the last in the sequence
                        # merge it with the first
                        second_gap_index = self.__find_gap_index(row,0)
    
                    else: 
                        # merge with the gap on the left
                        second_gap_index = self.__find_gap_index(row, gap_to_move+1)
                # remove the two gaps 
                self.__close_gap(row, gap_index)
                self.__close_gap(row, second_gap_index)
                # choose a random place and insert a gap
                # depending on left_or_right place a second gap on the left or right 
                new_gap = randint(0, self.seq_length-1)
                       
                
                if left_or_right == 0:
                    # insert a new gap on the left
                    if new_gap != 0:
                        self.__insert_gap(row, new_gap-1)
                        self.__insert_gap(row, new_gap)
                    else:
                        # gap is the first index of the sequence
                        # put the new gap to the right of it
                        self.__insert_gap(row, new_gap)
                        self.__insert_gap(row, new_gap+1)
                elif left_or_right == 1:
                    # insert a new gap on the right
                    if new_gap != self.seq_length-1:
                        self.__insert_gap(row, new_gap)
                        self.__insert_gap(row, new_gap+1)
                    else:
                        # the new gap is the last entery of the sequence
                        # place the gap on the left
                        self.__insert_gap(row, new_gap-1)
                        self.__insert_gap(row, new_gap)
            elif two_or_three == 3:
                # remove a gap at each side of the gap 
                # and insert three gaps together
                #print "Starting two_or_three = three"
                #print "gap_to_move ==", gap_to_move
                #print "num_of_gaps ==", num_of_gaps
                if gap_to_move == num_of_gaps:
                    # gap_to_move is the last gap 
                    # remove both gaps from  the left
                    left_gap = self.__find_gap_index(row, gap_to_move-2)
                    right_gap = self.__find_gap_index(row, gap_to_move-1)
                elif gap_to_move == 0:
                    # gap to move is the first gap
                    # remove two gaps from the right
                    right_gap = self.__find_gap_index(row, gap_to_move+2)
                    left_gap = self.__find_gap_index(row, gap_to_move+1)
                else:
                    # remove a gap from the left and the right 
                    left_gap = self.__find_gap_index(row, gap_to_move-1)
                    right_gap = self.__find_gap_index(row, gap_to_move+1)
                # remove the 3 gaps
                self.__close_gap(row, left_gap)
                self.__close_gap(row, gap_index)
                self.__close_gap(row, right_gap)
                
                # now the 3 gaps have been removed 
                # choose a place at random to insert a gap and 
                # insert a gap at the left and right
                
                other_new_gap = randint(0, self.seq_length-1)
                if other_new_gap == self.seq_length-1:
                    # the new gap is going at the very end of the sequence
                    # insert the other two gaps to the left
                    self.__insert_gap(row, other_new_gap-2)
                    self.__insert_gap(row, other_new_gap-1)
                    self.__insert_gap(row, other_new_gap)
                elif other_new_gap == 0:
                    #we want to insert a gap at the first place in the sequence
                    # place the two gaps to the right
                    self.__insert_gap(row, other_new_gap)
                    self.__insert_gap(row, other_new_gap+1)
                    self.__insert_gap(row, other_new_gap+2)
                else:
                    # insert the gap and put a gap on each side
                    self.__insert_gap(row, other_new_gap-1)
                    self.__insert_gap(row, other_new_gap)
                    self.__insert_gap(row, other_new_gap+1)
                    
        return self.alignment


    def __find_gap_index(self, row, gap_num):
        """
           Finds the index of a numbered gap

           TODO Fix bug it is possible for this not to return a value
           Then the index is set to None in the program
           leading to a crash
        """
        #print "In __find_gap_index", row, gap_num
        gap_count = 0
        for i, value in enumerate(self.alignment[row]):
            #count the gaps to find our randomly choosen gap
            if value == '-':                
                # we have found the correct gap
                # save its index and exit the loop 
                if gap_count == gap_num:
                    return i
                gap_count += 1
        return i
    def smart_gap_insertion(self):
        pass
    def smart_gap_shift(self):
        pass
    def smart_gap_merge(self):
        pass
    def gap_col_remover(self):
        pass
