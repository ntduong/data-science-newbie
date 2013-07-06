""" Problem 5: Unique trimming DNA sequences."""

import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
	# record[0]: seq id
	# record[1]: string of nucleotides
	nucleo = record[1][:-10]
	mr.emit_intermediate(nucleo, record[0])

def reducer(key, list_of_values):
    # key: trimmed nucleotide
    # value: 
	mr.emit(key)

if __name__ == '__main__':
	inputdata = open(sys.argv[1])
	mr.execute(inputdata, mapper, reducer)
