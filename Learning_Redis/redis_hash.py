""" Toy user-password storage using set and hash in Redis
    (c) Duong Nguyen @bed
"""

import redis
from hashlib import md5

def get_connection(host="localhost", port=6379, db=0):
    con = redis.Redis(host=host, port=port, db=db)
    if not con:
        return None
    return con
    
def add_user(con, username, age, pw):
    if con.sadd("users", username):
        con.hmset("user:%s" %username, {"age":age, "password":md5(pw).hexdigest()})
        return True
    else:
        print "Username already existed!"
        return False
        
def authenticate(con, username, pw):
    if con.sismember("users", username):
        hashed_pass = md5(pw).hexdigest()
        if hashed_pass == con.hget("user:%s" %username, "password"):
            return True
        else:
            print "Wrong password!"
            return False
    
    print "User not found!"
    return False

def remove_user(con, username):
    if con.sismember("users", username):
        con.srem("users", username)
        con.delete("user:%s" %username)
        return True
    else:
        print "User not found!"
        return False

def clear_all(con):
    print "Clear all users in the end of the world!"
    con.flushdb()
    
def test():
    con = get_connection()
    users = [("duong", "1", "xxxxx"), ("vivu", "25", "barca10"), ("roo", "27", "mu10")]
    
    for user in users:
        if not add_user(con, user[0], user[1], user[2]):
            print "Failed to add username %s" %user[0]
    
    if authenticate(con, "duong", "xxxxx"):
        print "Yeah! Got in!"
    else:
        print "Ooops!"
    
    remove_user(con, "vivu")
    if not authenticate(con, "vivu", "barca10"):
        print "vivu was removed!"
    else:
        print "Something wrong!"
    
    clear_all(con)
    
if __name__ == '__main__':
    test()
