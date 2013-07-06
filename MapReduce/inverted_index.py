""" Problem 1: Create inverted index. """
import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
	# record[0]: document id
	# record[1]: text of the document as a string
	doc_id = record[0]
	text = record[1]
	words = text.split()
	for w in words:
		mr.emit_intermediate(w, doc_id)

def reducer(key, list_of_values):
    # key: word
    # value: list of doc_ids
	total = set()
	for v in list_of_values:
		total.add(v)
	mr.emit((key, list(total)))

if __name__ == '__main__':
	inputdata = open(sys.argv[1])
	mr.execute(inputdata, mapper, reducer)
