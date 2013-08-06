import bottle
import socket

# localhost resolve
import socket
socket.getaddrinfo('localhost', 8080) 

@bottle.route("/")
def home_page():
	#return "<html><title>YEAH</title><body>Hello world\n</body></html>"
	mythings = ["c", "c++", "java", "python", "javascript"]
	return bottle.template("hello_world", username="duong", things=mythings)
	
@bottle.route("/testpage")
def test_page():
	return "This is a test page. How are you?"
	
bottle.debug(True)
bottle.run(host="localhost", port=8080)
