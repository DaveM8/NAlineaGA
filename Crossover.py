from random import randint
import copy

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
        self.p1_alignment = alignment1.np_alignment.copy()
        self.p2_alignment = alignment2.np_alignment.copy()

    def __chooseCrossover(self):
        """
           Choose at random which crossover to preform
        """
    def vertical(self):
        """
           Do a vertical crossover between the two parent alignments
           
           Return Two Alignments
          
        """
        # select a row at random
        split_col = randint(0, len(p1_alignment[0]))
        child_1 = self.p1_alignment.copy()
        # split the alignment at split_col
        # make a copy of the left side of the alignments
        left_child_1 = self.p1_alignment[:,:split_col].copy()
        #left_child_2 = self.p2_alignment[:,:split_col]
        
        # now I count the number of protines not including 
        # the gaps of each row on left_child_1 
        left_seq = []
        for line in left_child_1:
            line_num = 0
            for value in line:
                if value != '-':
                    line_num += 1
            left_seq.append(line_num)
        # now I go into alignment 2 
        # count the the correct number of protines
        # save the rest which will be right_child_1
        right_child_index = []
        for i, line in enumerate(p2_alignment):
            line_count = 0
            for j, value in enumerate(line):
                if value != '-':
                    line_count += 1
                    if line_count == left_seq[i]:
                        # save the index it's the start of right_child
                        right_child_index.append(j)
                    line_count += 1
        # now I've got the Index of the sequences which to create the
        # the right_seq
        for i in range(len(p1_alignmnet)):
            child_1[i,right_child_index[i]:] = /
                p2_alignment[i,right_child_index[i]].copy()
        self.p1.np_alignmnet = child_1.copy()
        return self.p1
    def horizontal(self):
        """
           Select a line at random and put the top of parent1 with the bottom of parent2
           And the bottom of perent2 with the top of parent1
           Return 2 alignments
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
    def matchenCol(self):
        """
           
        """
                p1_num_col = 0
        p2_num_col = 0
        p1_indexs = []
        p2_indexs = []
        # select the fully allinged columns
        # go throught both at the same time take note if one is
        # compleate and the other is not
        for i in range(len(self.p1_alignment)):
            p1_col = self.p1_alignment[:i]
            p2_col = self.p2_alignment[:i]

            p1_set = set(p1_col)
            p2_set = set(p2_col)

            if len(p1_set) == len(p2_set) == 1:
                # both cols are aligned 
                pass
            elif len(p1_set) == 1:
                # p1 is aligned
                # dont count columns of gaps
                if p1_set[0] != '-':
                    p1_num_col += 1
                    p1_indexs.append(i)
            elif len(p2_set) == 1:
                # p2 is aligned
                # dont count cloumns of gaps
                if p2_set[0] != '-':
                    p2_num_col += 1
                    p2_indexs.append(i)
        # so now I know how many and which columns are filled
