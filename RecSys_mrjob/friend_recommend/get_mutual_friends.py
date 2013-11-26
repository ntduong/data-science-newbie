'''
Created on 2013/09/29
@author: duong
'''

""" Given bidirectional friendship network data, compute mutual friends for each pair of people."""

from mrjob.job import MRJob

class MutualFriends(MRJob):
    
    def mapper(self, _, line):
        inp = line.split(',')
        user, friends = inp[0], inp[1:]
        for f in friends:
            if user < f:
                yield (user, f), friends
            else:
                yield (f, user), friends
                
    def reducer(self, key, values):
        key_out = "-".join(key)
        value_out = list(reduce(set.intersection, map(set, values)))
        yield key_out, value_out    
        
if __name__ == '__main__':
    MutualFriends.run()