'''
Created on 2013/09/29
@author: duong
'''

from mrjob.job import MRJob
import re

WORD_RE = re.compile(r"[\w']+")

class MRMostUsedWord(MRJob):
    
    def mapper_get_words(self, _, line):
        # emit (word, 1) for each word in line
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)
            
    def combiner_count_words(self, word, counts):
        # optimization: sum word counts so far
        yield (word, sum(counts))
        
    def reducer_count_words(self, word, counts):
        # send all (frequency, word) pairs to the same reducer (with key None)
        yield None, (sum(counts), word)
    
    def reducer_find_max_word(self, _, count_word_pairs):
        yield max(count_word_pairs)
    
    # In MrJob, a step consists of a mapper, a combiner, a reducer. 
    # All of those are optional, but at least one must be present.
    # Use mr() as below when more than one step are needed.
    def steps(self):
        return [
            self.mr(mapper=self.mapper_get_words, 
                    combiner=self.combiner_count_words,
                    reducer=self.reducer_count_words),
            self.mr(reducer=self.reducer_find_max_word)
        ]
        
if __name__ == '__main__':
    MRMostUsedWord.run()