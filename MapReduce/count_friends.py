""" Problem 3: Count the number of friends in given social network. """
import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    # record[0]: person 1
    # record[1]: person 2
    mr.emit_intermediate(record[0], 1)

def reducer(key, list_of_values):
    # key: person name
    # value: list of 1's
    mr.emit((key, sum(list_of_values)))

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
