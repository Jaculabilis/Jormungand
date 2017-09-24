import sys
import zmq
import json

class NetworkGate():
	def __init__(self, address, port):
		self._address = address
		self._port = port
		context = zmq.Context()
		self._socket = context.socket(zmq.REQ)
		self._socket.connect("tcp://{}:{}".format(address, port))
	
	def __repr__(self):
		return "[NetworkGate {}:{}]".format(self._address, self._port)
	
	def transmit(self, serial):
		s = json.dumps(serial)
		self._socket.send_string(s)
		message = self._socket.recv()