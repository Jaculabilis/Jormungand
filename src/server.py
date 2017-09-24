import sys
import zmq
import json
import time
from multiprocessing import Process, Queue
from Fishtank import Fishtank

def socket_listener(port, recv_queue):
	sys.stdout.write("Socket listener starting...\n")
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://*:{}".format(port))
	
	while True:
		message = socket.recv()
		response = b"Undefined response"
		try:
			serial = json.loads(message)
			if "class" in serial:
				sys.stdout.write("Listener received a {}\n".format(serial["class"]))
			recv_queue.put(serial, False)
			response = b"Received"
		except:
			response = b"Error"
		socket.send(response)

def main():
	port = int(sys.argv[1])
	sys.stdout.write("Launching on port {}\n".format(port))
	# Spawn the socket thread
	q = Queue()
	socket_proc = Process(target=socket_listener, args=(port,q))
	socket_proc.start()
	sys.stdout.write("Socket thread started\n")
	time.sleep(1)
	# Build the world
	fishtank = Fishtank(q)
	for i in range(1, len(sys.argv)):
		if sys.argv[i] == "-w":
			from entity.dummy.DebugWaiter import DebugWaiter
			fishtank.add_entity(DebugWaiter("DebugWaiter"))
		if sys.argv[i] == "-j":
			from entity.dummy.DebugJumper import DebugJumper
			fishtank.add_entity(DebugJumper("DebugJumper"))
		if sys.argv[i] == "-t":
			pipe_port = int(sys.argv[i+1])
			from network.NetworkGate import NetworkGate
			network_gate = NetworkGate("localhost", pipe_port)
			from entity.Tube import Tube
			fishtank.add_entity(Tube(network_gate))
	fishtank.run()

if __name__ == "__main__":
	main()