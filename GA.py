import numpy as np
from random import randint

import Alignment
import Mutate
from Crossover import Crossover
from Scoring import Scoring

class GA():
    def __init__(self,path_to_data, pop_size=50, num_generations=1000):
        """ class that creates the the pouplation of alignments
            and keeps track of the number of generations
        """
        self.gen_passed = 0
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.data_file = path_to_data
        self.population = []
        self.create_population()
        #self.run()
        self.indivdual_id = 0
        
    def selection(self):
        """
           Select which candates are kept till the next generation
           and which candates are used in crossover and mutation
        """
        pass
    def tournament(self):
        """ Run the tourment at the end of each generation always keeping
            the top 40% of the pouplation and selecting the best of
            the remaining 60%
        """
        # select a number of candidates for  
        pass
    def end_gen(self):
        # end of generation 
        # keep the top 40% of candidates
        pass
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
            self.population.append(my_alig)
            
    def run(self):
        """ 
           run the GA
           in each generation
               do some mutations 
               do some crossovers
               hold a tournment to decide which indiviuals I keep 
        """
        num_mutations = 2
        num_crossovers = 30

        # set up the pouplation
        for gen_num in range(self.num_generations):
            print "gen_num", gen_num
            # preform the mutations
            for i in range(num_mutations):
                pick_one = randint(0, self.pop_size-1)
                self.population[pick_one].mutation()

            for i in range(num_crossovers):
                p1 = randint(0, self.pop_size-1)
                p2 = randint(0, self.pop_size-1)
                while p1 == p2:
                    p2 = randint(0, self.pop_size-1)
                

                cross_over = Crossover(self.population[p1],
                                       self.population[p2])

                child_1, child_2 = cross_over.run()
                
                if child_1 != None:
                    self.population.append(child_1)
                if child_2 != None:
                    self.population.append(child_2)

        scores = []
        for candidate in self.population:
            line = []
            sum_of_pairs, identity = candidate.fittness()
            line.append(sum_of_pairs)
            line.append(identity)
            scores.append(line)
        
        sort = sorted(scores, key = lambda x:(x[0],x[1]))
        for line in sort:
            print line
        print len(sort)
            
    
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
       print alig_1.fittness()
       print alig_2.fittness()
       print "alig_1"
       alig_1.print_seq()
    
       print "alig_2"
       for i in range(40):
           alig_2.mutation()
       alig_2.print_seq()
       my_cross = Crossover(alig_1, alig_2)
       child_1, child_2 = my_cross.vertical()
       print "child_1"
       child_1.print_seq()
       print "child_2"
       child_2.print_seq()

       
       
       
my_ga = GA("1aho.rsf")
#my_ga.test()
my_ga.run()
