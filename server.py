import sys
import zmq
import time

if sys.argv[1] == "send":
	PORT = int(sys.argv[2])
	DEST = int(sys.argv[3])
	sys.stdout.write("Using port {}\n".format(PORT))
	sys.stdout.write("Connecting to port {}\n".format(DEST))
	
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://localhost:{}".format(DEST))
	
	while True:
		socket.send(b"Gentlemen.")
		message = socket.recv()
		sys.stdout.write("Response: {}\n".format(message))

if sys.argv[1] == "recv":
	PORT = int(sys.argv[2])
	sys.stdout.write("Using port {}\n".format(PORT))
	
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://*:{}".format(PORT))
	
	while True:
		message = socket.recv()
		sys.stdout.write("Received message: {}\n".format(message))
		time.sleep(1)
		socket.send(b"Received")