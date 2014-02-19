""" Problem 2: Implement a relational join."""

import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    # record[0]: table name (order or line_item)
    # record[1]: order_id
    # ....
    order_id = record[1]
    mr.emit_intermediate(order_id, record)

def reducer(key, list_of_values):
    # key: order_id
    # value: list of records
    for order in list_of_values:
        for line in list_of_values:
            if order[0] == 'order' and line[0] == 'line_item':
                join_value = []
                join_value.extend(order)
                join_value.extend(line)
                mr.emit(join_value)

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
