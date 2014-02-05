import numpy as np

class Sequence():
    def __init__(self, data):
        self.data = data
        self.make_np()
    def make_np(self):
        np_seq = np.ones([len(self.data),len(self.data[0][1])], dtype= np.string_)

        for i, line in enumerate(self.data):
            for j, my_char in enumerate(line[1]):
                #use '-' for spaces not '.'
                if my_char == '.': my_char = '-'
                np_seq[i][j] = my_char
        return np_seq
