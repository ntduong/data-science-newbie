'''
Created on 2013/09/29
@author: duong
'''

from mrjob.job import MRJob

""" Toy class to count the number of characters, words, lines in input file."""
class MRToyCount(MRJob):
    
    def mapper(self, _, line):
        yield "chars", len(line)
        yield  "words", len(line.split())
        yield  "lines", 1
        
    def reducer(self, key, values):
        yield key, sum(values)
        
if __name__ == '__main__':
    MRToyCount.run() # Note that, run() is a class method of MRToyCount (MRJob)        
        
    