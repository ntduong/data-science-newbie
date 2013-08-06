import pymongo

from pymongo import MongoClient

# connect to database
conn = MongoClient('localhost', 27017)
db = conn.test # test db

# get handle to names collection
names = db.names

item = names.find_one()

print item['name']