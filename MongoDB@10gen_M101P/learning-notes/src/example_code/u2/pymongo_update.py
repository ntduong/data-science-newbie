import pymongo
from pymongo import MongoClient
import sys
import datetime

def using_save(coll):
    print "Updating record using save..."
    try:
        score = coll.find_one({'student':0.0, 'type':'exam'})
        print 'before: ', score
        score['review_date'] = datetime.datetime.utcnow()   
        #coll.update({'student':0.0, 'type':'exam'}, score) # update
        #coll.save(score)
        #coll.update({'student':0.0, 'type':'exam'},{'$set':{'review_date':datetime.datetime.utcnow()}})
        
        score = coll.find_one({'student':0.0, 'type':'exam'})
        print 'after', score
        
    except:
        print "Unexpected error:", sys.exc_info()[0] 

def using_update(coll):
    pass

def main():
    conn = MongoClient("localhost", 27017)
    db = conn.test
    scores = db.scores
    
    using_save(scores)
    
if __name__ == '__main__':
    main()
    
    
