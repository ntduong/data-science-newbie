""" Problem 4: List all tuples of asymmetric friendship."""

import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    # record[0]: person 1
    # record[1]: person 2
    mr.emit_intermediate(tuple(sorted(record)), 1)

def reducer(key, list_of_values):
    # key: [person1, person 2]
    # value: list of 1's
    if sum(list_of_values) == 1:
        mr.emit((key[0],key[1]))
        mr.emit((key[1], key[0]))

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
