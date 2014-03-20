import numpy as np
from random import randint
import copy
import math

import Alignment
import Mutate
from Crossover import Crossover
from Scoring import Scoring

class GA():

    def __init__(self,path_to_data, pop_size=100, num_generations=500,
                 candidate_size = 2, comparison_size = 10, sigma_share = 3.14):
        """ class that creates the the pouplation of alignments
            and keeps track of the number of generations
        """
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.data_file = path_to_data
        self.population = {}
        self.create_population()
        self.candidate_size = candidate_size
        self.comparison_size = comparison_size
        self.sigma_share = 0
    
    def calc_sigma_share(self):
        """
           Calculate the value of sigma_share, the radius which
           repersents the size of the naighbiourhood 
           
        """
        q = 4
        SOP = []
        ID = []
        for key in self.population:
            sum_of_pairs, identity = self.normal_pop[key]
            #print sum_of_pairs, identity
            SOP.append(sum_of_pairs)
            ID.append(identity)
        
        
        max_min = 0
        max_min += (max(SOP) - abs(min(SOP))) ** 2
        max_min += (max(ID) - abs(min(ID))) ** 2
        
        r = (max_min ** 0.5) * 0.5
        
        share = float(r) / (q ** .5)
        share += 1
        if share == 0:
            share = 3.14
        return share

    def tournament(self):
        """ 
           run a binary tournament to select the best candation for mating
           returns the ID of the best candidate
        """
        # randomly choose a candidate set and a comparsion set
        candidates = []
        cand_set = set()
        comparison_set = set()
        comparison = []
        # sets are used to ensure 2 different indiviudals are chosen
        while len(cand_set) < self.candidate_size:
            cand_set.add(self.random_candidate())
        candidates = list(cand_set)

        while len(comparison_set) < self.comparison_size:
            comparison_set.add(self.random_candidate())
        comparison_set = list(comparison_set)


        candidate_score = {}
        total_score = 0
        for each in candidates:
            for j in comparison_set:
                total_score += self.dominates(each,j)
            candidate_score[each] = total_score
            total_score = 0
            
        scores = []
        for key, value in candidate_score.iteritems():
            line = []
            line.append(key)
            line.append(value)
            scores.append(line)

        scores = sorted(scores, key = lambda x: (x[1],x[0]))

        if len(scores) == 1:
            return scores[0][0]

        elif scores[-1][1] == scores[-2][1]:
            # they have the same score use sharing to reduce the fittness
            return self.share(scores[-1][0], scores[-2][0])
        else:
            # return the fittess candidate
            return scores[-1][0]
        print "Error"

    def share(self, cand_1, cand_2):
        """
           If there is a tie in the domination
           This function will reduce the fittness of candidates
           depending how many other candidats are in there neighborhood
        """

        # calculate the objective fittness of the soultions
        m1 = self.calc_dist(cand_1)
        m2 = self.calc_dist(cand_2)

        if m1 > m2:
            return cand_1
        elif m2 > m1:
            return cand_1
        else:
            # the soultions have equal sized naighbhoods choose one at random
            which = randint(1,2)
            if which == 1:
                return cand_1
            else:
                return cand_2

    def calc_dist(self,cand):
        """
            calculate the eculadian distiance of one point to every 
            other point in the population.
            Calculate the amount to reduce the fittness given how 
            many other soultions reside in the candidates nearbioughood

            takes: The candidate ID number
            returns: the size of the candidates naigberhood
        """
        

        dist = self.get_normal_fitness()
        self.sigma_share = self.calc_sigma_share()
        #dist = np.asarray(fit_list)
        cand_score = np.tile(self.normal_pop[cand], (len(dist),1))

        add_one = np.tile(1,(len(dist),1))
        cand_score[:,2:] += add_one
        dist[:,2:] += add_one
        dist[:,1:] -= cand_score
        dist[:,1:] = dist[:,1:] ** 2

        ans = np.zeros(len(dist[0]),float)
        ans = np.sum(dist[:,1:],1)
        ans = ans ** 0.5
        
        sh = 0
        
        #count = 0
        for i, value in enumerate(ans):
            if value <= self.sigma_share:
                sh += (1-(value / self.sigma_share))
                #count += 1
        #print "count", count
        return sh

    def get_normal_fitness(self):
        """
           get the fittness of all individuals in a normalised form
           All the values between 1 and 2 in the right proportion
           Used to calulate the neighbourhood
        """
        fit_list = []
        #print "current pop_size", len(self.population)
        # create a list with the fittness of the whole population
        for key in self.population:
            line = []
            line.append(key)
            SOP, ID = self.population[key].fittness()
            line.append(SOP)
            line.append(ID)
            fit_list.append(line)

        #put the values into an numpy array
        fit_values = np.asarray(fit_list, dtype = float)
        just_values = np.asarray(fit_values[:,1:], dtype = float)
        # normalise the values between 0 and 1 then add 1.
        # add one to identity to prevent divide by 0 error
        add_one = np.tile(1,(len(just_values),1))
        just_values[:,1:] += add_one
        min_value = just_values.min(0)
        max_value = just_values.max(0)
        min_minus = min_value = max_value
        normal = np.ones(np.shape(just_values))
        m = just_values.shape[0]
        normal = just_values - np.tile(min_value, (m,1))
        normal = normal/np.tile(min_minus, (m,1))
        
        for i, value in enumerate(fit_values):
            fit_values[i][1] = normal[i][0]
            fit_values[i][2] = normal[i][1]
        # put the normalized values back into a dictionary
        self.normal_pop = {}
        for i, values in enumerate(normal):
            self.normal_pop[fit_values[i][0]] = (values[0],values[1])
        return fit_values


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
        # they are equal
        return 0

    def gen_end(self):

        scores = []
        new_pop = {}
        for cand in self.population:
            line = []
            sum_of_pairs, identity = self.population[cand].fittness()
            line.append(sum_of_pairs)
            line.append(identity)
            line.append(cand)
            scores.append(line)

        sort_sums = sorted(scores,key =lambda x: (x[0]))
        sort_identity = sorted(scores,key = lambda x: (x[1]))
        for i in range(self.pop_size/2):
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
            # keep one copy of the original sequence
            if i != 0:
            # insert between 0 and 15 % of the length number of gaps
                mu = Mutate.Mutate(my_alig)
                num_gaps = randint(1, int(my_alig.length * 0.15))
                my_alig.np_alignment = mu.gap_insertion(num_gaps)
            # append the alignment object to the pouplation list
            self.population[my_alig.id] = my_alig
            

    def run(self):
        """ 
           run the GA
           in each generation
               do some mutations 
               do some crossovers
               hold a tournment to decide which indiviuals I keep 
        """
        # set up the pouplation
        for gen_num in range(self.num_generations):
            print "gen_num", gen_num, "pop size", len(self.population)
            if (gen_num % 50 == 0) or gen_num == self.num_generations-1:
                #print fittness values
                self.print_fittness(gen_num)
            # calculate the number of crossovers and mutations
            num_mutations =  int(len(self.population) * .4)
            num_crossovers = int(len(self.population) * .8)
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

                # matched_col will return None for child 2
                # and can return None for child 1 if both have the 
                # same aligned cols
                if child_1 != None:
                    self.population[child_1.id] = child_1
                if child_2 != None:
                    self.population[child_2.id] = child_2
            self.gen_end()

        scores = []
        new_pop = {}
        for cand in self.population:
            line = []
            sum_of_pairs, identity = self.population[cand].fittness()
            line.append(sum_of_pairs)
            line.append(identity)
            line.append(cand)
            scores.append(line)

        #print the fitest candidates
        sort_sums = sorted(scores,key =lambda x: (x[0]))
        sort_identity = sorted(scores,key = lambda x: (x[1]))

        print self.population[sort_sums[-1][2]].fittness()
        self.population[sort_sums[-1][2]].print_seq()

        print self.population[sort_identity[-1][2]].fittness()
        self.population[sort_identity[-1][2]].print_seq()

    def print_fittness(self, gen_num):
        """
           Print the values of the fittness individulas
           write them to a .csv file for use results
        """
        global file_name
        #file_name = self.data_file
        scores = []
        new_pop = {}
    
        for cand in self.population:
            line = []
            sum_of_pairs, identity = self.population[cand].fittness()
            line.append(sum_of_pairs)
            line.append(identity)
            line.append(cand)
            scores.append(line)

        sort_sums = sorted(scores,key =lambda x: (x[0]))
        sort_identity = sorted(scores,key = lambda x: (x[1]))

        best_sums, other_ID =  self.population[sort_sums[-1][2]].fittness()
        other_sums, best_ID =  self.population[sort_identity[-1][2]].fittness()

        result_file = file_name + "_results.csv"
        # open the file for appending
        open_file = open(result_file, 'a')
        file_line = str(gen_num) + "," + str(best_sums) + "," + str(best_ID) + '\n'
        open_file.write(file_line)
        print gen_num, best_sums, best_ID
        open_file.close()

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
            Padded with spaces.
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


file_name = "results/1aho_pop_100"
my_ga = GA("results/1aho.rsf")
#my_ga.test()
my_ga.run()
