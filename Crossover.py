from random import randint
import copy
import Alignment

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
        self.p1_alignment = self.p1.np_alignment.copy()
        self.p2_alignment = self.p2.np_alignment.copy()

    def __chooseCrossover(self):
        """
           Choose at random which crossover to preform
        """
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
        # select a row at random
        split_col = randint(0, len(self.p1_alignment[0]))
        # create the arrays to store the new alignments
        child_1 = self.p1_alignment.copy()
        child_2 = self.p2_alignment.copy()

        # split the alignment at split_col
        # make a copy of the left side of the alignments
        left_child_1 = self.p1_alignment[:,:split_col].copy()
        
        # count the number of letters on the left of p1
        # not including gaps
        left_seq = []
        for line in left_child_1:
            line_num = 0
            for value in line:
                if value != '-':
                    line_num += 1
            left_seq.append(line_num)

        # count the same number of protines in p2 
        # save the index that index gives a valad
        # sequence to put with the child alignments
        right_child_index = []
        
        for i, line in enumerate(self.p2_alignment):
            line_count = 0
            for j, value in enumerate(line):
                if value != '-':
                    line_count += 1
                    if line_count == left_seq[i]:
                        # save the index it's the start of right_child
                        right_child_index.append(j+1)    # +1 because of the way numpy indexes
        
        # use the correct indexs to create the two child alignments
        for i in range(len(self.p1_alignment)):
            #copy the right handside of p2 over the right handside of p1
            p1_new_right= self.p2_alignment[i,right_child_index[i]:].copy()
            child_1[i,right_child_index[i]:] = p1_new_right
            
            p2_new_right = self.p1_alignment[i,right_child_index[i]:].copy()
            child_2[i, right_child_index[i]:] = p2_new_right

        # create a new alignment to return
        child_alignment_1 = Alignment.Alignment(child_1, self.p1.names, self.p1.length)
        child_alignment_2 = Alignment.Alignment(child_2, self.p2.names, self.p2.length)
        return (child_alignment_1, child_alignment_2)

    def horizontal(self):
        """
           Select a line at random and put the top of parent1 with the bottom of parent2
           And the bottom of perent2 with the top of parent1
           Return 2 child alignments
        """
        # find out the number of rows
        num_rows = len(self.p1_alignment)
        # choose a crossover point
        # use 1 and num_rows-1 so the crossover point in inbetween two rows
        cross_point = randint(1,num_rows-1)
        p1_child = self.p2_alignment.copy()
        p2_child = self.p1_alignment.copy()
        print "cross_point ==", cross_point
        # replace all the lines after the crossover point with lines from p2
        for i in range(cross_point):
            if i < cross_point:
                p1_child[i] = self.p1_alignment[i].copy()
                p2_child[i] = self.p2_alignment[i].copy()
        self.p1.np_alignment = p1_child.copy()
        self.p2.np_alignment = p2_child.copy()
        return (self.p1, self.p2) 
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
        for i in range(len(self.p1_alignment[0])):
            p1_col = self.p1_alignment[:,i]
            p2_col = self.p2_alignment[:,i]

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

        #aligne a col in the parent with the lower identity socre
        # use the same trick of counting maybe
        if p1_num_col == p2_num_col:
            #same identity score choose on at random
            if p1_num_col == 0:
                # they have all the same aligned cols
                return None 
            which_one = randint(1,2)
            if which_one = 1:
                p1_num_col += 1
            elif which_one = 2:
                p2_num_col +=1
        if p1_num_col < p2_num_col:
            # line up a col in p1
            which_col = randint(0, p2_num_col)
            self.__match_the_col(self.p1, self.p2, which_col)
        elif p2_num_col < p1_num_col:
            #line up a col in p2
            which_col = randint(0, p1_num_col)
            self.__match_the_col(self.p2, self.p1, which_col)
        else:
            #should never get here
            print "Error"
    def __match_the_col(self, match, parent, which_col):
        """
           Do the work of matching a colume in an alignment
        """
