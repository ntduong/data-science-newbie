import pymongo
from pymongo import MongoClient
import sys

conn = MongoClient("localhost", 27017)
db = conn.students
grades = db.grades

try:
    cursor = grades.find({"type":"homework"})
    cursor = cursor.sort([("student_id", pymongo.ASCENDING), ("score", pymongo.ASCENDING)])
    student_id = -1
    for item in cursor:
        if item["student_id"] != student_id:
            student_id = item["student_id"]
            grades.remove(item)
        
except:
    print "Unexpected error:", sys.exc_info()[0]
    