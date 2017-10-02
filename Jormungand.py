import sys
from collections import defaultdict
from util.Util import logout

class Jormungand():
	def __init__(self, argv):
		command = argv[1] if len(argv) >= 2 else "help"
		registry = defaultdict(lambda: Jormungand.help, {
				"help": Jormungand.help,
				"run": Jormungand.run,
				"send": Jormungand.send
			})
		exec_func = registry[command]
		self.execute = lambda: exec_func(argv)
	
	@staticmethod
	def help(argv):
		print("Hello, world!")
	
	@staticmethod
	def run(argv):
		if len(argv) < 3:
			print("run requires a port")
			sys.exit(-1)
		port = int(argv[2])
		from world.Server import Server
		server = Server(port)
		logout("Launching server on port {}".format(port), "Jormungand run")
		server.run(argv[3:])
	
	@staticmethod
	def send(argv):
		if len(argv) < 4:
			print("send requires a target and payload")
			sys.exit(-1)
		address = argv[2]
		import zmq, json, pygame
		pygame.display.set_mode((1,1), pygame.NOFRAME)
		context = zmq.Context()
		socket = context.socket(zmq.REQ)
		socket.connect("tcp://{}".format(address))
		for i in range(3, len(argv)):
			if argv[i] == "-ball":
				from entity.dummy.DebugBall import DebugBall
				e = DebugBall()
				s = json.dumps(e.serialize())
				print("Sending {}".format(str(e)))
				for i in range(100):
					socket.send_string(s)
					message = socket.recv()
				print("Reply: {}".format(message))

def main():
	j = Jormungand(sys.argv)
	j.execute()

if __name__ == "__main__":
	main()