from random import randint
import copy
import Alignment
import numpy as np
class Crossover():
    """ class to carry out crossover on an alignment
        their are 3 crossover operators one is randomly 
        selected and preformed between two parents to
        produce two child alignmets
    """
    def __init__(self, alignment1, alignment2):
        
        # use copy.copy() to get a copy of the objects
        # so we do not alter the parents with the crossover
        self.p1 = copy.copy(alignment1)
        self.p2 = copy.copy(alignment2)
        #make copys of the original seqences
        #self.p1_alignment = self.p1.np_alignment.copy()
        #self.p2_alignment = self.p2.np_alignment.copy()

    def run(self):
        """
           Choose at random which crossover to preform
        """
        which = randint(1,3)
        if which == 1:
           return  self.vertical()
        elif which == 2:
            return self.horizontal()
        else:
            return self.matched_col()

    def vertical(self):
        """
           Do a vertical crossover between the two parent alignments
           
           Return Two child Alignments
           
           Choose a position at random and create two child alignments by
           putting the left side of p1 with the right side of p2
           Because the order of the alignments must remain the same
           I count the number of letters not including the gaps on
           the left side of one of the parents, then to get the
           index to cut the other parent at count the same number
           of letters again not including gaps this gives the correct
           index to cut and create the correct child alignments
           with the correct sequences.
          
        """
        try:
        # select a col at random
            split_col = randint(0, self.p1.length)
            # create the arrays to store the new alignments
            child_1 = np.ones_like(self.p2.np_alignment, dtype = np.string_)
            child_2 = np.ones_like(self.p1.np_alignment, dtype = np.string_)
            # split the alignment at split_col
            # make a copy of the left side of the alignments
            left_child_1 = self.p1.np_alignment[:,:split_col].copy() # copys everthing before split_col

            # count the number of letters on the left of p1
            # not including gaps
            left_seq = []
            for line in left_child_1:
                letter_num = 0
                for value in line:
                    if value != '-':
                        letter_num += 1
                left_seq.append(letter_num)
            # count the same number of letters in p2 
            # save the index, that index gives a valad
            # sequence to put with the child alignments
            p2_index = []

            for i, line in enumerate(self.p2.np_alignment):
                line_count = 0
                for j, value in enumerate(line):
                    if value != '-':
                        line_count += 1
                        if line_count == left_seq[i]:
                            # save the index it's the start of right_child
                            p2_index.append(j+1)    # +1 because of the way numpy indexes


            # use the correct indexs to create the two child alignments
            for i in range(len(self.p1.np_alignment)):

                child_1_left = self.p1.np_alignment[i,:split_col].copy()
                child_2_left = self.p2.np_alignment[i,:p2_index[i]].copy()

                child_1_right = self.p2.np_alignment[i,p2_index[i]:].copy()
                child_2_right = self.p1.np_alignment[i,split_col:].copy()

                child_1[i,:split_col] = child_1_left
                child_1_right.resize(len(child_1[i,split_col:]))
                child_1[i,split_col:] = child_1_right

                child_2_right.resize(len(child_2[i,p2_index[i]:]))
                child_2[i,:p2_index[i]] = child_2_left
                child_2[i,p2_index[i]:] = child_2_right


            # create a new alignment to return
            #np_child_1 = np.asarray(child_1, dtype = np.string_)
            #np_child_2 = np.asarray(child_2, dtype = np.string_)
            child_alignment_1 = Alignment.Alignment(child_1, self.p1.names)
            child_alignment_2 = Alignment.Alignment(child_2, self.p2.names)
            return (child_alignment_1, child_alignment_2)
        except IndexError:
            return None, None
            

    def horizontal(self):
        """
           Select a line at random and put the top of parent1 with the bottom of parent2
           And the bottom of perent2 with the top of parent1
           Return 2 child alignments
        """
        # find out the number of rows
        num_rows = len(self.p1.np_alignment)
        # choose a crossover point
        # use 1 and num_rows-1 so the crossover point in inbetween two rows
        cross_point = randint(1,num_rows-1)
        p1_child = self.p2.np_alignment.copy()
        p2_child = self.p1.np_alignment.copy()
        #print "cross_point ==", cross_point
        # replace all the lines after the crossover point with lines from p2
        for i in range(cross_point):
            if i < cross_point:
                p1_child[i] = self.p1.np_alignment[i].copy()
                p2_child[i] = self.p2.np_alignment[i].copy()
        #self.p1.np_alignment = p1_child.copy()
        #self.p2.np_alignment = p2_child.copy()
        child_alignment_1 = Alignment.Alignment(p1_child, self.p1.names)
        child_alignment_2 = Alignment.Alignment(p2_child, self.p2.names)
        return (child_alignment_1, child_alignment_2) 
    def matched_col(self):
        """
           choose a fully aligned column from from one of the parents
           which is not fully aligned in the other and add or remove
           gaps until it is fully aligned

           Return one child alignment
        """
        p1_num_col = 0
        p2_num_col = 0

        p1_indexs = []
        p2_indexs = []
        # select the fully allinged columns
        # go throught both at the same time take note if one is
        # complete and the other is not
        for i in range(len(self.p1.np_alignment[0])):
            p1_col = self.p1.np_alignment[:,i]
            p2_col = self.p2.np_alignment[:,i]
            
            p1_set = set(p1_col)
            p2_set = set(p2_col)
            
            if len(p1_set) == len(p2_set) == 1:
                # both cols are aligned 
                pass
            elif len(p1_set) == 1:
                # p1 is aligned
                # dont count columns of gaps
                if p1_col[0] != '-':
                    p1_num_col += 1
                    p1_indexs.append(i)
            elif len(p2_set) == 1:
                # p2 is aligned
                # dont count cloumns of gaps
                if p2_col[0] != '-':
                    p2_num_col += 1
                    p2_indexs.append(i)

        #aline a col in the parent with the lower identity socre
        if p1_num_col == p2_num_col:
            #same identity score choose one at random
            if p1_num_col == 0:
                # they have all the same aligned cols
                return None, None
            
        if p1_num_col < p2_num_col:
            # line up a col in p1
            which_col = randint(0, p2_num_col-1)
            child = self.__match_the_col(self.p1, self.p2, p2_indexs[which_col])

        elif p2_num_col < p1_num_col:
            #line up a col in p2
            which_col = randint(0, p1_num_col-1)
            child = self.__match_the_col(self.p2, self.p1, p1_indexs[which_col])
        else:
            # they have equal number of matched cols
            # choose one at random
            p1_or_p2 = randint(1,2)
            if p1_or_p2 == 1:
                 which_col = randint(0, p2_num_col-1)
                 child = self.__match_the_col(self.p1, self.p2, p2_indexs[which_col])
            else:
                #line up a col in p2
                which_col = randint(0, p1_num_col-1)
                child = self.__match_the_col(self.p2, self.p1, p1_indexs[which_col])

        return child, None

    def __match_the_col(self, p1, p2, which_col):
        """
           Do the work of matching a colume in an alignment
        """
        # count the number of letters on each line
        # not including gaps up until which_col +1
        left_child = p2.np_alignment[:,:which_col+1].copy()
        for line in left_child:
            print ''.join(line)
        # first count the correct number of letters to the fully aligned col in p2
        letter_num = []
        for line in left_child:
            letter_count = 0
            for j, value in enumerate(line):
                if value != '-':
                    letter_count += 1
            letter_num.append(letter_count)

        # next find the index of that letter in p1
        index = []
        print letter_num
        for line in p1.np_alignment:
            print ''.join(line)
        for i, line in enumerate(p1.np_alignment):
            letter_count = 0
            for j, value in enumerate(line):
                if value != '-':
                    letter_count += 1
                    if letter_count == letter_num[i]:
                        index.append(j)
                        break

        # find which line the letter has the highest index
        largest_index_value = 0
        largest_index_line = 0
        print "index", index
        for i, value in enumerate(index):
            if value > largest_index_value:
                largest_index_value = value
                largest_index_line = i
        print "lagerst_index", largest_index_line
        # move all the other lines to that index 
        for line_num, line in enumerate(p1.np_alignment):
            if line_num != largest_index_line:
                num_gaps = largest_index_value - index[line_num]
                for j in range(num_gaps):
                    self.__insert_gap(p1, line_num, index[line_num]+j)
        #return the alignment with the extra aligned column
        return p1, None


    def __insert_gap(self, alignment, row, col):
        """
           take care of inserting a gap in an alignment
           at position row, col
        """
        #print "Inserting gap at", row, col
        # make a copy of the rest of the row droping the last '-'
        rest_of_col = alignment.np_alignment[row][col:-1].copy()
        #insert a gap '-'
        alignment.np_alignment[row][col] = '-'
        # put the rest of the row back after the gap '-'
        alignment.np_alignment[row][col+1:] = rest_of_col
    def remove_col_gaps (self):
        """
           Remove any cols which contain only gaps
        """
