import numpy as np
from random import randint
import copy

import Alignment
import Mutate
from Crossover import Crossover
from Scoring import Scoring

class GA():
    def __init__(self,path_to_data, pop_size=50, num_generations=1000, candidate_size = 2, comparison_size = 4):
        """ class that creates the the pouplation of alignments
            and keeps track of the number of generations
        """
        self.gen_passed = 0
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.data_file = path_to_data
        self.population = {}
        self.create_population()
        self.candidate_size = candidate_size
        self.comparison_size = comparison_size
        
        
    def selection(self):
        """
           Select which candates are kept till the next generation
           and which candates are used in crossover and mutation
        """
        pass
    def tournament(self):
        """ 
           run a tournament to select the best candation for mating
           currently it returns the last candidate if there is a draw
           TODO handbags at dawn if it is a tie
        """
        # randomly choose a candidate set and a comparsion set
        candidates = []
        comparison_set = []
        for i in range(self.candidate_size):
            candidates.append(self.random_candidate())
        
        for i in range(self.comparison_size):
            comparison_set.append(self.random_candidate())

        candidate_score = {}
        total_score = 0
        for each in candidates:
            for j in comparison_set:
                total_score += self.dominates(each,j)
            candidate_score[each] = total_score
            total_score = 0
        
        high_score = 0
        winner = candidates[0]
        for each in candidates:
            if candidate_score[each] > high_score:
                high_score = candidate_score[each]
                #print "high_score", high_score 
                winner = each
        return winner
                
    def dominates(self,cand_1, cand_2):
        """
           Return 2 cand_1 fully dominates cand_2
                  1 cand_1 partly dominates cand_2
                 -1 cand_2 fully dominates cand_1
                  0 they are equal

        """
        cand_1_SOP, cand_1_ID = self.population[cand_1].fittness()
        cand_2_SOP, cand_2_ID = self.population[cand_2].fittness()
        
        # cand 1 fully dominates cand 2
        if cand_1_SOP > cand_2_SOP and cand_1_ID > cand_2_ID:
            return 2
        # cand 1 partly dominates cand 2
        if cand_1_SOP > cand_2_SOP:
            return 1
        # cand 1 partly dominates cand 2
        if cand_1_ID > cand_2_SOP:
            return 1
        # cand 2 fully dominates cand 1
        if cand_2_SOP > cand_1_SOP and cand_2_ID > cand_1_SOP:
            return -1
        # thay are equal
        return 0
        
    def gen_end(self):
        # end of generation 
        # keep the 50  candidates with the best sum-of-pairs
        # keep the 
        scores = []
        new_pop = {}
        #for line in self.population:
            #print line
        for cand in self.population:
            line = []
            sum_of_pairs, identity = self.population[cand].fittness()
            line.append(sum_of_pairs)
            line.append(identity)
            line.append(cand)
            scores.append(line)
        
        sort_sums = sorted(scores, key = lambda x:(x[0],x[1]))
        sort_identity = sorted(scores, key = lambda x:(x[1],x[0]))
        for i in range(50):
            new_pop[sort_sums[-i][2]] = self.population[sort_sums[-i][2]]
            new_pop[sort_identity[-i][2]] = self.population[sort_identity[-i][2]]

        self.population = new_pop
    def create_population(self):
        """
           Create the pouplation 
           Read the files 
           Create a list containing Alignment objects 
        """
        # read the sequence from file
        np_seq, seq_names = self.read_data()
        for i in range (self.pop_size):
            
            # create an Alignment object with the data
            my_alig =  Alignment.Alignment(np_seq, seq_names)
            # append the alignment object to the pouplation list
            self.population[my_alig.id] = my_alig
        self.start = copy.copy(self.population[0])    
    def run(self):
        """ 
           run the GA
           in each generation
               do some mutations 
               do some crossovers
               hold a tournment to decide which indiviuals I keep 
        """
        num_mutations = 20
        num_crossovers = 10

        # set up the pouplation
        for gen_num in range(self.num_generations):
            print "gen_num", gen_num, "pop size", len(self.population)
            # preform the mutations
            for i in range(num_mutations):
                pick_one = self.random_candidate()
                self.population[pick_one].mutation()

            for i in range(num_crossovers):
                
                p1 = self.tournament()
                p2 = self.tournament()
                while p1 == p2:
                    p2 = self.tournament()
                
                    
                cross_over = Crossover(self.population[p1],
                                       self.population[p2])

                child_1, child_2 = cross_over.run()

                if child_1 != None:
                    self.population[child_1.id] = child_1
                if child_2 != None:
                    self.population[child_2.id] = child_2
            self.gen_end()

        scores = []
        for candidate in self.population:
            line = []
            sum_of_pairs, identity = self.population[candidate].fittness()
            line.append(sum_of_pairs)
            line.append(identity)
            scores.append(line)
        
        sort_sum = sorted(scores, key = lambda x:(x[0],x[1]))
        sort_identity = sorted(scores, key = lambda x:(x[1],x[0]))

        for key in self.population:
            print "candidate ID", key
            self.population[key].print_seq()
            print self.population[key].fittness()
            print len(self.population[key].np_alignment[0])
        print
        self.start.print_seq()
        print self.start.fittness()
    def random_candidate(self):
        """
           Return a random candidate ID
        """
        keys = self.population.keys()
        rand_one = randint(0, len(keys)-1)
        return keys[rand_one]

    def read_data(self):
        """ Read The sequences to be alinged. 
            BAliBASE set of aligments will be used to test algorithim
            the .rsf file format will be used 
            
            This method Reads a .rsf file
            returns  a data structure with mutiple sequences
            Padded with spaces to be aligned.
        """
        openfile = open(self.data_file, "r")

        seq_name = []       # a list containing the name of the sequence
        seq_value = []       # a list to store each sequence   
        seq_flag = False    # if we are on the sqeuence data keep reading sequence data until } is reached
        seq_str = ""        # used to get the compleate sequence on one line in the list
        max_len = 0         # stores the length of the longest sequence used to prevent the
                            # operators selecting the padded gaps

        for line in openfile:
            line = line.strip()
            line = line.split(' ')
            #save the name for identification 
            if line[0] =='name':
                # the last value in the line will be the name of the sequence
                seq_name.append(line[-1])
                continue
            #all the lines after 'sequence' are part of the sequence
            if line[0] == 'sequence':
                seq_flag = True
                continue
            #check that we have not come to the end of the sequence and we are reading the sequence
            if(line[0] != '}' and seq_flag):
                # Keep appending each line of the sequence data to a string
                seq_str += line[0]

            # we have finished reading the sequence append the compleate sequence 
            # to seq_name and reset all the vairiblaes
            if line[0] == '}':
                #we are at the end of a sequence
                seq_value.append(seq_str)
                current_len = len(seq_str)
                if current_len > max_len:
                    max_len = current_len
                seq_flag = False
                seq_str = ""
        # close the file
        openfile.close()
        
        # Save the sequences in a numpy array for fast proccessing
        # make the array 25% lager to give room to add gaps
        np_seq = np.ones([len(seq_value), max_len*1.25], dtype= np.string_)
        
        seq_length = len(seq_value[0])
        # go throught the list and add every char to np_seq
        # also replace . used in BAliBASE with - used for alinaiGA
        for i, line in enumerate(seq_value):
            for j, my_char in enumerate(line):
                #use '-' for spaces not '.'
                if my_char == '.': my_char = '-'
                np_seq[i][j] = my_char
        #replace the padded ones with .
        for i,line in enumerate(np_seq):
            for j, my_char in enumerate(line):
                if my_char == '1':
                    np_seq[i][j] = '-'
        return np_seq, seq_name

    def test(self):
       alig_1 = self.population[0]
       alig_2 = self.population[1]
       alig_1.print_seq()
       for i in range(10):
           alig_1.mutation()
       
       alig_1.print_seq()
       #alig_1.remove_gap_col()
       print
       alig_1.print_seq()

       
       
       
my_ga = GA("1aho.rsf")
#my_ga.test()
my_ga.run()
