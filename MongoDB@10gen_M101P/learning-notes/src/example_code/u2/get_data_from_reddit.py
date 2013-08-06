import json
import urllib2
import pymongo
from pymongo import MongoClient
import sys

def insert_reddit_into_mongo(coll):
    #reddit = urllib2.urlopen("http://www.reddit.com/r/technology/.json")
    with open("reddit.json", "r") as reddit:
        parsed = json.loads(reddit.read())
    
    for item in parsed['data']['children']:
        coll.insert(item['data'])

def regex_query(coll, keyword):
    query = {'title':{'$regex':keyword}}
    projection = {'title':1, '_id':0}

    try:
        iter = coll.find(query, projection)
        
    except:
        print "Unexpected error:", sys.exc_info()[0]

    return iter
        
def find_video_url(coll):
    """ Example of using dot notation."""
    query = {'media.oembed.type':'video'}
    projection = {'media.oembed.url':1, '_id':0}
    
    try:
        iter = coll.find(query, projection)
        
    except:
        print 'Unexpected error:', sys.exc_info()[0]
    
    return iter

def main():
    conn = MongoClient("localhost", 27017)
    # get a handle to a reddit db
    db = conn.reddit
    # get a handle to a stories collection in reddit db
    stories = db.stories
    
    iter = find_video_url(stories)
    for item in iter:
        print item
        
        
    
if __name__ == '__main__':
    main()