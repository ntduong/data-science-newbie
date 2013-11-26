'''
Created on 2013/09/29
@author: Duong Nguyen @TokyoTech
'''

""" Simple friend recommendation in bidirectional friendship network."""

from mrjob.job import MRJob

class BiDirFriendsRecommend(MRJob):
    
    def mapper_input(self, key, line):
        inp = line.split(",")
        user, friends = inp[0], inp[1:]
        n_friends = len(inp[1:])
        
        for f in friends:
            if user < f:
                yield ((user, f), -1)
            else:
                yield ((f, user), -1)
        
        for i in xrange(n_friends):
            for j in xrange(i+1, n_friends):
                if friends[i] < friends[j]:
                    yield ((friends[i], friends[j]), 1)
                else:
                    yield ((friends[j], friends[i]), 1)
    
    def reducer_count_mutual_friends(self, key, values):
        
        if -1 in values: # ignore pairs that are already friends
            return
        
        f1, f2 = key
        yield ((f1, f2), sum(values))
        
    def mapper_2(self, key, value):
        """ 
            Input: (key, value) pairs as below, obtained from above reducer.
                key: (f1, f2)
                value: # mutual friends of f1, and f2.
            Output: 
                (f1, [f2, # mutual friends of f1 and f2])
                (f2, [f1, # mutual friends of f1 and f2])
        """
        f1, f2 = key
        yield (f1, (f2, int(value)))
        yield (f2, (f1, int(value)))
        
    def reducer_top_rec(self, key, values):
        """ 
            Input: 
                key: f
                values: list of pairs (fi, # mutual friends of f and fi)
            Output:
                key: f
                value: top_k recommendations for f 
        """
        TOP_K = 3
        rec_list = [p for p in values]
        yield key, sorted(rec_list, key=lambda val: -val[1])[:TOP_K]
        
    def steps(self):
        return [
            self.mr(mapper=self.mapper_input, 
                    reducer=self.reducer_count_mutual_friends),
            self.mr(mapper=self.mapper_2,
                    reducer=self.reducer_top_rec)
        ]
        
if __name__ == '__main__':
    BiDirFriendsRecommend.run()