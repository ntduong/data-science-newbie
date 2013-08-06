import pymongo
from pymongo import MongoClient
import sys

conn = MongoClient("localhost", 27017)
db = conn.school
people = db.people

doc = {"name":"Andrew Ng", "company":"google","interest":["AI","ML","deep learning"]}

try:
    people.insert(doc)
    print doc # pymongo automatically insert _id into doc!!!
    # people.insert(doc) --> duplicate doc insertion error
    
    
except: 
    print "Unexpected error:", sys.exc_info()[0]