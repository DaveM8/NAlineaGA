import numpy as np
import Alignment
import Mutate

class GA():
    def __init__(self,path_to_data, pop_size=20, num_generations=1000):
        """ class that creates the the pouplation of alignments
            and keeps track of the number of generations
        """
        self.gen_passed = 0
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.data_file = path_to_data
        self.np_seq, self.seq_names, self.seq_length = self.read_data()
    def tournament(self):
        """ Run the tourment at the end of each generation always keeping
            the top 40% of the pouplation and selecting the best of
            the remaining 60%
        """
        pass
    def run(self):
        """ Run the GA 
            Read the data file
            create the pouplation of Alignment objects
            keep track of the generation number
            at the end of each generation run the tournamint
        """
        self.population = []
        # set up the pouplation
        for i in range(self.pop_size):
            a = Alignment.Alignment(self.np_seq, self.seq_names)
            self.population.append(a)
    def print_seq(self):
        """
            print out the sequences as nice strings
        """
        for i, line in enumerate(self.np_seq):
            #print the name of the sequence and the values of the sequence
            my_str = ''.join(line)
            new_str = ''
            for j, char in enumerate(my_str):
                new_str += char
                if j % 10 == 0 and j != 0:
                    new_str += ' '
            print self.seq_names[i] , new_str


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
                seq_flag = False
                seq_str = ""
        # close the file
        openfile.close()
        
        # Save the sequences in a numpy array for fast proccessing
        # make the array 25% lager to give room to add gaps
        np_seq = np.ones([len(seq_value),len(seq_value[0])*1.25], dtype= np.string_)
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
        return np_seq, seq_name, seq_length
    def test(self):
       my_alig =  Alignment.Alignment(self.np_seq, self.seq_names, self.seq_length)
       #score = my_alig.identity()
       #print score
       my_alig.mutation()

        
my_ga = GA("1aho.rsf")
my_ga.print_seq()
my_ga.test()
print
my_ga.print_seq()
