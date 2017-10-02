import zmq
import json
import time
from multiprocessing import Process, Queue
from world.Fishtank import Fishtank
from util.Util import logout

class Server(object):
	def __init__(self, recv_port):
		self.recv_port = recv_port
		self.recv_queue = Queue()
		self.recv_proc = Process(
			target=self.socket_listener,
			args=(self.recv_port, self.recv_queue))
	
	def socket_listener(self, port, recv_queue):
		logout("Socket thread starting", "Server.socket_listener")
		context = zmq.Context()
		socket = context.socket(zmq.REP)
		socket.bind("tcp://*:{}".format(port))
		
		while True:
			message = socket.recv()
			response = b"Undefined response"
			try:
				serial = json.loads(message)
				if "class" in serial:
					logout("Received: {}".format(serial["class"]), "Server.socket_listener")
				recv_queue.put(serial, False)
				response = b"Received"
			except:
				response = b"Error"
			socket.send(response)

	def run(self, argv):
		# Launch the recv process
		self.recv_proc.start()
		logout("Socket thread launched", "Server")
		time.sleep(0.2)
		
		# Build the world
		fishtank = Fishtank(self.recv_queue)
		
		for i in range(len(argv)):
			if argv[i] == "-ball":
				from entity.dummy.DebugBall import DebugBall
				fishtank.add_entity(DebugBall())
			if argv[i] == "-tube":
				tube_port = int(argv[i+1])
				from world.NetworkGate import NetworkGate
				network_gate = NetworkGate("localhost", tube_port)
				from entity.Tube import Tube
				fishtank.add_entity(Tube(network_gate))
		fishtank.run()