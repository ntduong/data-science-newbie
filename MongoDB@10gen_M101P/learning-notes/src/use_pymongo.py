"""
    Play with mongodb using pymongo
    (c) Duong Nguyen @Home
"""

import pymongo
from pymongo import MongoClient
import random
from collections import defaultdict

def make_data(coll, n_docs=50):
    coll.insert([
        dict(x=random.random(), y=random.randint(0,10)) for _ in xrange(n_docs)
    ])
    
def do_aggregate(db, coll_name='temp'):
    pipeline = [
        {"$group" : {
            "_id" : "$y",
            "mean_x" : {"$avg" : "$x"}}
        }
    ]
    
    res = db.command("aggregate", coll_name, pipeline=pipeline)
    if res['ok']:
        for item in res["result"]:
            print item
    
def main_temp():
    client = MongoClient("localhost", 27017) # connect to given host through given port
    db = client.test
    coll = db.temp
    make_data(coll, n_docs=50)
    
    '''
    cs = coll.find()
    for doc in cs:
        print doc
    print "%d documents in total" %(coll.count())
    '''
    do_aggregate(db, "temp")
    
def update_stuff():
    client = MongoClient("localhost", 27017)
    db = client.test
    coll = db.stuff
    coll.update({"a":2}, {"$push":{"b":7}})
    
    print coll.find_one({"a":2})
    
if __name__ == '__main__':
    update_stuff()