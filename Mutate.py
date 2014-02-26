import numpy as np
from Scoring import Scoring
from random import randint

# A class to carry out mutations on the alignment
class Mutate():
    """
        Provide matation operators
        Returns a mutated np_alignment data structour
    """
    def __init__(self, alignment,  num_gaps = 1,
                       smart_retry = 3, smart_dir_prob = 50):

        self.obj = alignment           # the alignment object to be mutated
        self.alignment = alignment.np_alignment     # the alignment to be mutated
        self.length = alignment.length
        self.num_gaps = num_gaps       # the number of gaps to insert in gap_insertion()
        self.smart_retry = smart_retry # number of retrys used in smart operators
        self.seq_length = alignment.length
        self.smart_dir_prob = smart_dir_prob
        #self.choose_oper()
    
    def __insert_gap(self, row, col):
        """
           take care of inserting a gap in an alignment
           at position row, col
        """
        print "Inserting gap at", row, col
        # make a copy of the rest of the row droping the last '-'
        rest_of_col = self.alignment[row][col:-1].copy()
        #insert a gap '-'
        self.alignment[row][col] = '-'
        # put the rest of the row back after the gap '-'
        self.alignment[row][col+1:] = rest_of_col
        # calulate the new length and update it
        self.obj.update_length()
        self.length = self.obj.length


    def __close_gap(self, row, cols):
        """
           Remove a gap from position row, col
           col is a list so I can look after the the removal of
           many gaps at once here
        """
        
        # sort the list of gaps to be removed
        cols.sort()
        # reverse the list so we always remove the right most
        # gaps first to prevent the indexs shifting when we
        # remove "lefter" gaps
        cols.reverse()
        for col in cols:
            print "Removing gap at", row, col
            # copy all the data after the gap
            row_after_gap = self.alignment[row][col+1:].copy()
            #place that data in the row starting where the gap was
            self.alignment[row][col:-1] = row_after_gap
            #insert the gap at the end of the row
            self.alignment[row][-1] = '-'
            # calculate the new length and update the current length
            self.obj.update_length()
            self.length = self.obj.length()

    def choose_oper(self):
        """
            randomly choose which if any operator is used on the alignment 
        """
        
        # First try a even odd for the mutation
        rand_num = randint(1,3)
        
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
        
    def gap_insertion(self,num_gaps = 5):
        """
           insert num_gaps number of gaps at a random possition
           in each row
        """
        print "Start length", self.length
        for i, line in enumerate(self.alignment):
            for j in range(num_gaps):
                position = randint(0,self.length)
                self.__insert_gap(i, position)
        print "End length", self.length
        return self.alignment

    def gap_shift(self, all_lines = True):
        """
           randomly choose a gap and move it to another position
           if all lines is set to true gaps will be shifited on every line
           if al_lines is False (default) one line will be selected at random
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
            for i in range (0, self.length+1):
                if self.alignment[row][i] == '-':
                    num_of_gaps += 1
            # randomly choose one of the gaps
            gap_to_move = randint(0,num_of_gaps)
            #find index of gap to move
            gap_count = 0
            gap_index = 0
            # no need to use self.length here because we will find our gap before that
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
            self.__close_gap(row,[gap_index])
            #choose a random position and insert a gap
            new_gap = randint(0, self.length)
            self.__insert_gap(row, new_gap)
        return self.alignment

    def gap_merge(self, all_lines = False):
        """
           Select 2 or 3 consective  gaps at random and merge
           them into one consective gap. then move them to a random position
           
           This version selects a gap at random and either takes 
           a gap at either side of the next gap on the left or right
           removes them and inserts 2 or 3 gaps in a sequence at a random
           position.
           
           It may be intresting to move throught a row and select 2 or 3 
           consective gaps and move them.
           
           NOTE when removing 2 gaps if the randomly selected gap is the first or last 
           it will be mearged with a gap at the start for the last or the end for last
           
           But when removing 3 gaps the 3 gaps will always be at the same end
           Maybe I'll change this later

           NOTE look into how __insert_gap works to make sure I dont lose letters
           when palcing new gaps 
        """
        # count the gaps 

        # create a list of all the rows or just one 
        # randomly choosen row
        rows = []
        if all_lines:
            # all lines is true, merge and move gaps on all lines
            for i, line in enumerate(self.alignment):
                rows.append(i)
        else:
            # choose one row at random
            rows.append(randint(0, len(self.alignment)-1))
        
        for row in rows:
            # count the number of gaps start at zero
            num_of_gaps = -1
            for value in self.alignment[row]:
                if value == '-':
                    num_of_gaps += 1
        
            two_or_three = randint(2,3)
            # choose a gap at random
            # if we want 3 take the gap on each side
            # if we want 2 take one from right or left at random
            
            # randomly choose a gap 
            gap_to_move = randint(0, num_of_gaps)
            # find the index of the gap 
            gap_index = self.__find_gap_index(row, gap_to_move)
    
            if two_or_three == 2:
                # we are going to merge 2 gaps
                left_or_right = randint(0,1)
            
                if left_or_right == 0:
                    #look for a gap on the left
                    if gap_to_move == 0:
                        # the gap is the first gap in the sequence
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
                self.__close_gap(row, [gap_index, second_gap_index])
                
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
                self.__close_gap(row, [left_gap,gap_index,right_gap])
                
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
                # have we have found the correct gap
                if gap_count == gap_num:
                    return i
                gap_count += 1
   
    def __better_alignment(self, test_alignment):
        """
           evaluate if an alignment is better that another
           in one of sum of pairs or identity and better
           or the same in the other

           return True test_alignment is better than self.alignment
                  False self.alignment is better
        """
        
        test_score = Scoring(test_alignment, self.length)
        self_score = Scoring(self.alignment, self.length)

        test_identity = test_score.identity()
        test_sum_of_pairs = test_score.sum_of_pairs()
        #print "test", test_identity, test_sum_of_pairs

        self_identity = self_score.identity()
        self_sum_of_pairs = self_score.sum_of_pairs()

        print  self_identity, ',', self_sum_of_pairs
        if self_identity > test_identity and self_sum_of_pairs >= test_sum_of_pairs:
            return True
        if self_sum_of_pairs > test_sum_of_pairs and self_identity >= test_identity:
            return True
        return False

    def smart_gap_insertion(self,smart_num_gaps = 1, attempts = 10000 ):
        """
           Choose a position at random insert a gap
           then insert a gap at the start or end of every other row
           
           check if the alignment has been improved only keep if 
           alignment is improved on one of sum-of-pairs or
           identity
        """
        #TODO Could I get an oveflow if I go Over The edge with a gap

        # make a copy of the alignment to work on
        old_alignment = self.alignment.copy()

        for trys in range(attempts):      
            # choose a random position
            row = randint(0, len(self.alignment)-1)
            col = randint(0, self.seq_length)
            
            # insert a gap in the random position
            self.__insert_gap(row, col)
            # choose a side to insert the gaps in the other rows
            # each generation it starts at 5 
            # if the mutation improves the alignment 1 is added
            # if the mutation makes the alignment worst 1 is subtracted
            # the higher the value of smart_dir_prob the more lickily
            # it that gaps are inserted at the start of the sequence

            start_or_end = randint(1,100)
            if start_or_end <= self.smart_dir_prob:
                #add the gaps at the start
                start = True
            else:
                #add the gaps at the end
                start = False

            for i, line in enumerate(self.alignment):
                # do not add a gap at the start of the row we added already
                if i == row: continue
                if start == True:
                    self.__insert_gap(i, 0)
                else:
                    self.__insert_gap(i, self.seq_length)
                    
            # test to see if the new alignment is better
            if self.__better_alignment(old_alignment):
                print "Found Better"
                # if I'm keeping the new alignment do nothing
                return self.alignment
            else:
                # revert to the origianl alignment
                self.alignment = old_alignment.copy()
            if start:
                # last time we placed gaps at the start 
                # we have droped that so subtract 1 from smart_dir_prob
                # so next time it will be more likely to add gaps at the end
                self.smart_dir_prob -= 1
            else:
                self.smart_dir_prob +=1
        #print "Keeping alignment"
        #return old_alignment
        # do not return any value set the self.alignment to old_alignment
        print "no better alignment found"
        return old_alignment
    def smart_gap_shift(self, attempts = 3):
        """
           choose a gap at random and move it in a random direction
           TODO This can get an IndexError if I Try to shift a gap 
           near the end NEED to fix this
        """

        # make a copy of the strating aligment
        old_alignment = self.alignment.copy()
        # choose a row at random
        row = randint(0,len(self.alignment)-1)

        # count the gaps on the row
        num_of_gaps = 0
        for value in self.alignment[row]:
            if value == '-':
                num_of_gaps += 1
        # randomly choose one of the gaps
        gap_to_move = randint(0,num_of_gaps)
        # get the index of the gap to be moved
        gap_index = self.__find_gap_index(row, gap_to_move)
        
        #close the gap
        self.__close_gap(row, [gap_index])
        
        # insert a gap to the left or right
        # check if the alignment is better 
        # try this attempts number of times
        for trys in range(attempts):
            # choose a direction using smart_dir_prob
            left_or_right = randint(1,100)
            if left_or_right <= self.smart_dir_prob:
                #add the gaps at the start
                left = True
            else:
                #add the gaps at the end
                left = False

            if left:
                # insert gaps to the left of gap_index
                # add the extra 1 because trys starts at 0
                new_gap_index = gap_index - trys - 1
                #prevent an underflow
                while new_gap_index <= 0:
                    new_gap_index += 1

                print row, new_gap_index
                self.__insert_gap(row, new_gap_index)
            else:
                # insert a gap to the right
                new_gap_index = gap_index + trys + 1
                #prevent an overflow by moving a gap from the end
                while new_gap_index >= len(self.alignment[0])-1:
                    new_gap_index -= 1
                print row, new_gap_index
                self.__insert_gap(row, new_gap_index)
            # check if the new alignment is better if so keep it
            # if not close the gap and try another to the left or right
            print
            for line in self.alignment:
                print ''.join(line)
            if self.__better_alignment(old_alignment):
                return self.alignment
            else:
                #  adjest probility of moving left or right
                if left:
                    self.smart_dir_prob -= 1
                else:
                    self.smart_dir_prob += 1
                # 
                self.alignment = old_alignment.copy()
        return old_alignment
        
            
    def smart_gap_merge(self, attempts = 3):
        """
           call gap_merge but only keep the alignment if it improves
        """
        old_alignment = self.alignment.copy()
        
        for trys in range(attempts):
            self.gap_merge()
            if __better_alignment(old_alignment):
                return self.alignment
            else:
                self.alignment = old_alignment.copy()
        #return old_alignment        
        # return to the original alignment
        self.alignment = old_alignment

   
