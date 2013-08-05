"""
    Getting my hands dirty with Redis 
    Note: Using redis-py module for Python (e.g: easy_install redis)
    Check out: 
    + https://github.com/andymccurdy/redis-py/ for more details
    + http://redis-py.readthedocs.org/en/latest/ for API
    
    Note: Make sure to start a redis server beforehand, using e.g. redis-server command
    (c) Duong Nguyen @moon
"""

import redis


def get_connection(host="localhost", port=6379, db=0):
    """ Get connection to a given db @host:port.
        By default: default db (number 0), localhost:6379
    """
    # connect to db 0 (default) in a redis server @localhost:6379
    con = redis.Redis(host=host, port=port, db=db) 
    assert con, "Something wrong!"
    return con

def simple_set(con, key, val, overwrite=False):
    """ Simple set for given key-value pair.
        Params:
            overwrite: True to overwrite the value of already existed key.
    """
    
    assert con, "No connection!"
    if (not con.get(key)) or overwrite:
        con.set(key, val) 
    else:
        print "Do nothing!"
    
def simple_get(con, key):
    """ Simple get using given key."""
    assert con, "No connection!"
    if con.exists(key):
        return con.get(key)
    return None
        
def simple_test(con):
    key = "person"
    value = "{name:duong, planet:moon}"
    simple_set(con, key, value, overwrite=False)
    print simple_get(con, key)
    new_value = "{name:nguyen, planet:earth}"
    simple_set(con, key, new_value, overwrite=True)
    print simple_get(con, key)
    if not simple_get(con, "duong"):
        print "Not found"
    
    print "Get all keys in the current db before flushing:"
    print con.keys(pattern="*")
    con.flushdb()
    print "After flushing:"
    print con.keys(pattern="*")
    
def test_ds(con):
    """ Try out data structures in Redis."""
    pass

if __name__ == '__main__':
    con = get_connection()
    #simple_test(con)
    

