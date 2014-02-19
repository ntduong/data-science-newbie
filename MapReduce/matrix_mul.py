""" Problem 6: Matrix multiplication
    Two matrices A, B are given in a sparse format, 
    where each record is (i,j,value) (the element at row i, col j is value)
    Compute C = A x B and return C in sparse format.
    One-step algorithm is implemented below.
"""

import MapReduce
import sys

mr = MapReduce.MapReduce()

# Hardcode the dimension of input matrices A, B
NROW_A = 10
NCOL_B = 10

def mapper(record):
    """ 
        Input: a record formatted as [matrix, i, j, value], where
            + matrix: string, specifies which matrix the record comes from ('a' or 'b')
            + i,j: row,column
            + value: element at row i, column j
        Output: a pair of key-value as below
            + ['a', i, j, A_ij] -> [(i,k),(A, j, A_ij)] for k = 1,...,#cols(B)
            + ['b', i, j, B_ij] -> [(k,j),(B, j, B_ij)] for k = 1,...,#rows(A) 
    """
    mat,r,c,val = record # unpack record
    if mat == 'a':
        for k in range(NCOL_B):
            mr.emit_intermediate((r,k), (mat,c,val))
    elif mat == 'b':
        for k in range(NROW_A):
            mr.emit_intermediate((k,c), (mat,r,val))    
    
def reducer(key, list_of_values):
    val = 0
    for item_a in list_of_values:
        for item_b in list_of_values:
            if item_a[0] == 'a' and item_b[0] == 'b':
                if item_a[1] == item_b[1]:
                    val += item_a[2] * item_b[2]
    if val != 0:
        mr.emit((key[0], key[1], val))
    
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
