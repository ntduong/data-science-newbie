""" Toy user-password storage program using set in Redis.
    Reference: http://degizmo.com/2010/03/23/redis-relations-in-a-nosql-world/
    
    (c) Duong Nguyen @moon
"""

import redis
from hashlib import md5

def get_connection(host="localhost", port=6379, db=0):
    con = redis.Redis(host=host, port=port, db=db)
    if not con:
        return None
    return con
    
def add_user(con, username, fullname, password):
    """ Note: Each user has an unique username. """
    if con.sadd("users", username): # return True if user is not existed in current db
        con.set("user:%s:fullname" %username, fullname)
        con.set("user:%s:password" %username, md5(password).hexdigest())
        return True
    else:
        print "Username already existed!"
        return False
        
def authenticate(con, username, password):
    if con.sismember("users", username):
        hashed_pass = md5(password).hexdigest()
        if hashed_pass == con.get("user:%s:password" %username):
            return True
        else:
            print "Wrong password!"
            return False
    
    print "User not found!"
    return False

def remove_user(con, username):
    if con.sismember("users", username):
        con.srem("users", username) # remove from set
        con.delete("user:%s:fullname" %username) # delete by key
        con.delete("user:%s:password" %username) 
        return True
    else:
        print "User not found!"
        return False
    
def clear_all(con):
    print "Clear all users in the end of the world!"
    con.flushdb()

def test():
    con = get_connection()
    users = [("duong", "duong nguyen", "xxxxx"), ("messi", "lionel messi", "barca10"), ("rooney", "wayne rooney", "mu10")]
    
    for user in users:
        if not add_user(con, user[0], user[1], user[2]):
            print "Failed to add username %s" %user[0]
    
    if authenticate(con, "duong", "abcxyz"):
        print "Yeah! Got in!"
    else:
        print "Ooops!"
    
    remove_user(con, "messi")
    if not authenticate(con, "messi", "barca10"):
        print "Messi was removed!"
    else:
        print "Something wrong!"
    
    clear_all(con)
    
if __name__ == '__main__':
    test()