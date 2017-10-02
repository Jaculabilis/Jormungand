import sys
import zmq
import json
from util.Util import logout

class NetworkGate():
	def __init__(self, address, port):
		self.address = address
		self.port = port
		context = zmq.Context()
		self.socket = context.socket(zmq.REQ)
		self.socket.connect("tcp://{}:{}".format(address, port))
	
	def __repr__(self):
		return "[NetworkGate {}:{}]".format(self.address, self.port)
	
	def transmit(self, serial):
		s = json.dumps(serial)
		logout("Sending: {}".format(serial["class"]))
		self.socket.send_string(s)
		message = self.socket.recv()