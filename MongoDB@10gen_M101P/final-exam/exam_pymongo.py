"""
   MongoDB Final Exam 
   (c) Duong Nguyen @Home
"""

import pymongo
from pymongo import MongoClient
from collections import defaultdict

def question_1():
    client = MongoClient("localhost", 27017)
    db = client.enron
    coll = db.messages
    print coll.find({"headers.From":"andrew.fastow@enron.com", "headers.To":"jeff.skilling@enron.com"}).count()
    #print count_msg("andrew.fastow@enron.com", ["jeff.skilling@enron.com"])
    
def aggregate_enron(from_user):
    client = MongoClient("localhost", 27017)
    db = client.enron
    coll = db.messages
    
    pipeline = [
        {"$match":{
            "headers.From": from_user 
        }},
        {"$unwind":"$headers.To"},
        {"$group":{"_id":"$_id", "TO":{"$addToSet":"$headers.To"}}},
        {"$unwind":"$TO"}
    ]
    
    res = db.command("aggregate", "messages", pipeline=pipeline)
    if res["ok"]:
        return res["result"]
    else:
        return None
   
    
def count_msg(from_user, to_users):
    result = aggregate_enron(from_user)
    assert result, "NONE!"
    msg_cnt = defaultdict(int)
    for user in to_users:
        for msg in result:
            if msg['TO'] == user:
                msg_cnt[user] += 1
                            
    return msg_cnt
   
def question_2():
    '''
    from_user = "susan.mara@enron.com"
    to_users = ["jeff.dasovich@enron.com", "richard.shapiro@enron.com", 
                "james.steffes@enron.com", "alan.comnes@enron.com"]
    from_user = "soblander@carrfut.com"
    to_users = ["soblander@carrfut.com"]
    '''
    from_user = "evelyn.metoyer@enron.com"
    to_users = ["kate.symes@enron.com"]
    msg_cnt = count_msg(from_user, to_users)
    for user in to_users:
        print 'From %s To %s: %d' %(from_user, user, msg_cnt[user])
   
def question_3(msg_id="<8147308.1075851042335.JavaMail.evans@thyme>"):
    client = MongoClient("localhost", 27017)
    db = client.enron
    coll = db.messages
    print 'Before update:'
    item = coll.find_one({"headers.Message-ID":msg_id})
    print len(item["headers"]["To"])
    print item["headers"]["To"]
    coll.update({"headers.Message-ID" : msg_id}, {"$push" : {"headers.To" : "mrpotatohead@10gen.com"}})
    #coll.update({"headers.Message-ID" : msg_id}, {"$pop" : {"headers.To" : 1}})
    print 'After update:'
    item = coll.find_one({"headers.Message-ID":msg_id})
    print len(item["headers"]["To"])
    print item["headers"]["To"]

def question_7():
    client = MongoClient("localhost", 27017)
    db = client.test
    images = db.images
    albums = db.albums
    
    n_images = images.count()
    
    img_ids = []
    for album in albums.find():
        img_ids.extend(album['images'])
        
    orphant_ids = set(xrange(n_images)) - set(img_ids)
    
    pipeline = [
        {"$match" : {"tags" : "kittens"}},
        {"$project":{"_id" : 1}}
    ] 
    
    res = db.command("aggregate", "images", pipeline=pipeline)
    if res["ok"]:
        kitten_ids = set([item['_id'] for item in res["result"]]) 
    else:
        kitten_ids = set([])
    
    print len(kitten_ids - orphant_ids) # 44822
    
    
if __name__ == '__main__':
    question_7()



