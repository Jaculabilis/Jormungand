import sys
from entity.Entity import Entity

class Tube(Entity):
	def __init__(self, network_gate):
		Entity.__init__(self)
		self._gate = network_gate
		self._inbox = []
	
	def __repr__(self):
		return "[Tube gate={} inbox={}]".format(repr(self._gate), repr(self._inbox))
	
	def accept(self, entity):
		self._fishtank.remove_entity(entity)
		self._inbox.append(entity)
	
	def update(self):
		Entity.update(self)
		if self._inbox:
			entity = self._inbox.pop(0)
			sys.stdout.write("Sending: {}\n".format(repr(entity)))
			self._gate.transmit(entity.serialize())