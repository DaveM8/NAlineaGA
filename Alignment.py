###############################################################################
# Alignment.py - An object to repersent a multiple sequence alignment
#
###############################################################################
# based on the work of
# da Silva, F. J. M.J., Perez, J. M. S.M., Pulido, J. A. G.A.,
# and Rodriguez, M. V.A. (2011).
# Parallel niche pareto AlineaGA-an evolutionary multiobjective
# approach on multiple sequence alignment.
# Journal of integrative bioinformatics, 8(3).
###############################################################################
# Copyright (C) David Morrisroe 2014
# pizzadave108 at gmail dot com
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
###############################################################################


from Mutate import Mutate
import Scoring
import numpy as np

number = 0
class Alignment():
    def __init__(self, np_alignment, names):
        """
           Set up the object to preform an aligment
        """
        global number
        self.np_alignment = np_alignment
        self.names = names
        self.id = number
        number += 1
        self.changed = False
        self.score_of_pairs = None
        self.score_identity = None
    
    def same_alignment(self, other_aligment):
        """
           Verifiy that another alignment is the same not including
           gaps
        """
        # create a string of all the letters in the alignment 
        # with no gaps these should be the same on both alignments
        str_1 = ''
        str_2 = ''
        for line in self.np_alignment:
            for value in line:
                if value == '-' or value == '':
                    pass
                else:
                    str_1 += value

        for line in other_alignment.np_alignment:
            for value in line:
                if value == '-' or value == '':
                    pass
                else:
                    str_2 += value
        same = True
        for value in enumerate(str_1):
            if value == str_2[i]:
                pass
            else:
                print "Error", value, "!=", str_2[i]
                same = False
        return same

    @property
    def last_start(self):
        """
           Return the index of the row with the most gaps at the start
           before a letter.
           Needed in Crossover.vertical because if i try to split
           the alignment on cols that has no letters at on the left
           I'll get index errors
        """
        max_gaps = 0
        # count in from the end 
        for i, line in enumerate(self.np_alignment):
            current_len = 0
            for j in range(len(self.np_alignment[i])-1):
                if self.np_alignment[i][j] == '-':
                    current_len += 1
                else:
                    if current_len > max_gaps:
                        max_gaps = current_len
                    # only want the first letter on a line so break
                    break
        return max_gaps
    @property
    def short_length(self):
        """
           Return the length of the shortest sequence in the alignment
           Nesseary in Crossover.vertical() because if I pick a column
           to split which has only gaps left on one or more of the
           lines then I have no index the letter
        """
        max_gaps = 0
        # count in from the end 
        for i, line in enumerate(self.np_alignment):
            current_len = 0
            for j in range(len(self.np_alignment[i])-1, 0, -1):
                if self.np_alignment[i][j] == '-':
                    current_len += 1
                else:
                    if current_len > max_gaps:
                        max_gaps = current_len
                    # only want the first letter on a line so break
                    break
        # return the length of the shortest line
        min_len = len(self.np_alignment[0])-1 - max_gaps
        return min_len

        
    @property
    def length(self):
        """
           return the length of the longest sequence in the alignment
           used to avoid selecting the padding rows with operators

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
        return max_len

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
        if not self.changed and self.score_of_pairs is not None and self.score_identity is not None:
            return self.score_of_pairs, self.score_identity

        score = Scoring.Scoring(self)

        self.score_of_pairs = score.sum_of_pairs()
        self.score_identity = score.identity()
        
        self.changed = False
        return self.score_of_pairs, self.score_identity

    def mutation(self, smart = True):
        """ preform one of the six mutations at random 
            on the aligment. by pasing the data to a
            mutation object
        """
        self.changed = True
        mu = Mutate(self)
        self.np_alignment = mu.choose_oper()
        self.remove_gap_col()

    def remove_gap_col(self):
        """
           remove all columns containing only gaps
 
        """
        # go throught the alignment as far as  self.length
        # and remove any colums which contain only rows
        col_index = []
        for i in range(self.length):
            col = self.np_alignment[:,i]
            col_set = set(col)
            if len(col_set) == 1 and col[0] == '-':
                #the col contains only gaps remove it
                col_index.append(i)
        col_index.sort()
        col_index.reverse()
        for col in col_index:
            self.remove_col(col)

    def remove_col(self, col):
        
        # copy all the cols after the one we want to remove
        right = self.np_alignment[:,col+1:].copy()
        # write that copy back starting at the col to be removed
        self.np_alignment[:,col:-1:] = right
        # make the last col gaps
        self.np_alignment[:,-1:] = '-'
        
        
