# pymongo for CRUD
import pymongo
from pymongo import MongoClient
import sys


conn = MongoClient("localhost", 27017)
db = conn.test
scores = db.scores

query = {'type':'exam'}
selector = {'student':1, 'score':1, '_id':0} # field projection (selection)
'''
try:
    items = scores.find(query, selector) # note that items is currently Cursor obj
    for i, item in enumerate(items):
        if i >= 10: break
        print item
    
except:
    print "Unexpected error: ", sys.exc_info()[0]
'''
 
query = {'type':'quiz', 'score':{'$gt':20, '$lt':90}}
try:
    items = scores.find(query, selector)
    for i, item in enumerate(items):
        if i >= 10: break
        print item
        
except:
    print "Unexpected error: ", sys.exc_info()[0]