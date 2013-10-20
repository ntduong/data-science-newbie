""" Toy Implementation of Consistent Hashing for learning purpose.
    Reference: http://michaelnielsen.org/blog/consistent-hashing
"""

import bisect
import hashlib

class ConsistentHash(object):
    def __init__(self, n_machines=1, n_replicas=1):
        self.n_machines = n_machines
        self.n_replicas = n_replicas
        hash_tuples = [(i, j, get_hash(str(i) + "_" + str(j))) 
                        for i in xrange(n_machines)
                        for j in xrange(n_replicas)]
                        
        hash_tuples.sort(key=lambda x: x[2]) # in-place sort by hash value
        self.hash_tuples = hash_tuples
    
    def get_machine(self, key):
        """ Compute the machine and replica number for given key."""
        h = get_hash(key)
        if h > self.hash_tuples[-1][2]: # large than the largest hash value --> back to first hash value
            return self.hash_tuples[0][0]
        hash_values = [item[2] for item in self.hash_tuples]
        index = bisect.bisect_left(hash_values, h) # binary search to get machine index
        return self.hash_tuples[index][0], self.hash_tuples[index][1]
    
    def __repr__(self):
        ret = [] # sorted by machine number, then replica number
        for m, r, hv in sorted(self.hash_tuples, key=lambda t: (t[0], t[1])):
            ret.append("Hash value for machine %d, replica %d: %f" %(m, r, hv))
        return "\n".join(ret)
        
        
def get_hash(key, algo="md5"):
    """ Get hash value for given key using specified algorithm.
        Normalize hash value into [0,1) range.
        @param algo: Specify hashing algorithm. 
    """
    h = hashlib.new(algo)
    h.update(key)
    return (int(h.hexdigest(), 16) % 1000000)/1000000.0

def test(nm, nr, key_list, verbose=False):
    """ Testing consistent hashing.
        @param nm: The number of machines 
        @param nr: The number of replicas
        @param key_list: List of keys to insert
        @param verbose: Print out consistent hashing or not  
    """
    test_ch = ConsistentHash(nm, nr)
    if verbose:
        print test_ch
        print "-" * 30
        print test_ch.hash_tuples
    
    for k in key_list:
        m, r = test_ch.get_machine(k)
        print ("Key '%s' with hash value '%f' is mapped to machine %d replica %d\n" 
                %(k, get_hash(k), m, r))
        
if __name__ == "__main__":
    test(7,3, ["cpp", "python", "java", "ruby", "R", "matlab"])