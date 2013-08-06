import pymongo
from pymongo import MongoClient


def get_next_seq_number(name):
    conn = MongoClient("localhost", 27017)
    db = conn.test
    counters = db.counters
    
    counter = counters.find_and_modify(query={'type':name},
                                        update={'$inc':{'value':1}},
                                        upsert=True, new=True)
                                        
    counter_value = counter['value']
    return counter_value
    
    
if __name__ == '__main__':
    for i in xrange(10):
        print get_next_seq_number('uid')
        
    