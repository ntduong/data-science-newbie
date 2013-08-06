import bottle
import pymongo

# localhost resolve
import socket
socket.getaddrinfo('localhost', 8082) 

# Default path of the web server

@bottle.route("/")
def index():
	# connect to mongoDB
	conn = pymongo.MongoClient('localhost', 27017)
	
	# attach to test db
	db = conn.test
	
	# get handle to names collection in test db
	names = db.names
	
	item = names.find_one()
	
	return "<b> Hello %s!</b>" % item['name']
	
bottle.run(host='localhost', port=8082)
	