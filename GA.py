import numpy as np
from random import randint
import copy

import Alignment
import Mutate
from Crossover import Crossover
from Scoring import Scoring

class GA():
    def __init__(self,path_to_data, pop_size=20, num_generations=500,
                 candidate_size = 2, comparison_size = 10, sigma_share = 3.14):
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
        self.sigma_share = sigma_share
    
    #@property
    #def sigma_share(self):
    #    """
    #       Calculate the value of sigma_share, the radius which
    #       repersents the size of the naighbiourhood 
    #       
    #    """
    #    q = 4
    #    inside = 
    #    r 0.5*(()** 0.5
    def selection(self):
        """
           Select which candates are kept till the next generation
           and which candates are used in crossover and mutation
        """
        pass
    def tournament(self):
        """ 
           run a binary tournament to select the best candation for mating
           retuens the ID of the best candidate
        """
        # randomly choose a candidate set and a comparsion set
        candidates = []
        cand_set = set()
        comparison_set = set()
        comparison = []
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
        #print "len(scores)", len(scores)
        #print scores
        #print scores[-1][1], scores[-2][1]

        if len(scores) == 1:
            return scores[0][0]

        elif scores[-1][1] == scores[-2][1]:
            # they have the same score use sharing to reduce the fittness
            #print scores[-1][0],scores[-2][0]
            return self.share(scores[-1][0], scores[-2][0])
        else:
            # return the fittess candidate
            return scores[-1][0]
        print "Error"

    def share(self, cand_1, cand_2):
        """
           Handbags at Dawn
           If there is a tie in the domination
           This function will reduce the fittness of candidates
           depending how many other candidats are in there neighborhood
        """
        # calculate the fittness scores of all the population
        self.all_scores = {}
        for key in self.population:
            self.all_scores[key] = self.population[key]
        # get the values of the two candidates 
        cand_1_SOP, cand_1_ID = self.all_scores[cand_1].fittness()
        cand_2_SOP, cand_2_ID = self.all_scores[cand_2].fittness()
        
        # calculate the objective fittness of the soultions
        m1 = self.calc_dist(cand_1)
        m2 = self.calc_dist(cand_2)
        
        if m1 > m2:
            return cand_1
        elif m2 > m1:
            return cand_1
        else:
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
            retuens: A
        """
        fit_list = []
        for key in self.population:
            line = []
            line.append(key)
            SOP, ID = self.population[key].fittness()
            line.append(SOP)
            line.append(ID)
            fit_list.append(line)
        
        dist = np.asarray(fit_list)
        cand_score = np.tile(self.population[cand].fittness(), (len(dist),1))
        #print cand_score
        add_one = np.tile(1,(len(dist),1))
        #print add_one.shape
        cand_score[:,2:] += add_one
        dist[:,2:] += add_one
        #print dist[:,2:]
        dist[:,1:] -= cand_score
        dist[:,1:] = dist[:,1:] ** 2

        ans = np.zeros(len(dist[0]),float)
        ans = np.sum(dist[:,1:],1)
        ans = ans ** 0.5
        #print ans
        sh = 0
        #count = 0
        #print len(ans)
        for i, value in enumerate(ans):
            #print "value", value
            if value <= self.sigma_share:
                #count += 1
                sh += (1-(value / self.sigma_share))
        #print count, " in the naibourhood"
        return sh
    

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

        #scores = sorted(scores, key = lambda x: (x[1],x[0]))
        sort_sums = sorted(scores,key =lambda x: (x[0]))
        sort_identity = sorted(scores,key = lambda x: (x[1]))
        for i in range(10):
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
        self.population[1].print_seq()
        print self.population[1].fittness()
        self.start = copy.copy(self.population[1])

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
            #print "gen_num", gen_num, "pop size", len(self.population)
            if gen_num % 50 == 0 and gen_num != 0:
                #print fittness metreixs for reuslts section
                self.print_fittness(gen_num)
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

                if child_1 != None:
                    self.population[child_1.id] = child_1
                if child_2 != None:
                    self.population[child_2.id] = child_2
            self.gen_end()


        #for key in self.population:
        #    print "candidate ID", key
        #    self.population[key].print_seq()
        #    print self.population[key].fittness()
        #    print len(self.population[key].np_alignment[0])
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

        #scores = sorted(scores, key = lambda x: (x[1],x[0]))
        sort_sums = sorted(scores,key =lambda x: (x[0]))
        sort_identity = sorted(scores,key = lambda x: (x[1]))
        print self.population[sort_sums[-1][2]].fittness()
        self.population[sort_sums[-1][2]].print_seq()
        print self.population[sort_identity[-1][2]].fittness()
        self.population[sort_identity[-1][2]].print_seq()
    def print_fittness(self, gen_num):
        global file_name 
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

        #scores = sorted(scores, key = lambda x: (x[1],x[0]))
        sort_sums = sorted(scores,key =lambda x: (x[0]))
        sort_identity = sorted(scores,key = lambda x: (x[1]))

        best_sums, other_ID =  self.population[sort_sums[-1][2]].fittness()
        other_sums, best_ID =  self.population[sort_identity[-1][2]].fittness()
        
        result_file = file_name + "_results.csv"
        # open the file for appending
        open_file = open(result_file, 'a')
        file_line = gen_num + "," + best_sums + "," + best_ID + '\n'
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
       print alig_1.fittness()

file_name = 'results/1fjlA'
my_ga = GA("1aho.rsf")
#my_ga.test()
my_ga.run()
