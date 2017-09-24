import sys
from entity.Entity import Entity
from entity.Tube import Tube

class DebugJumper(Entity):
	def __init__(self, message):
		Entity.__init__(self)
		self._message = message
		self._counter = 0
	
	def __repr__(self):
		return "[DebugJumper message='{}' counter={}]".format(self._message, self._counter)
	
	def serialize(self):
		sup = Entity.serialize(self)
		sup.update({
			"module":"entity.dummy.DebugJumper",
			"class":"DebugJumper",
			"message":self._message,
			"counter":self._counter
		})
		return sup
	
	@staticmethod
	def deserialize(serial):
		e = DebugJumper(serial["message"])
		e._counter = serial["counter"]
		return e
	
	def update(self):
		Entity.update(self)
		self._counter += 1
		if self._counter % 5 == 0:
			for entity in self._fishtank._entities:
				if type(entity) is Tube:
					entity.accept(self)
					break
	
	def draw(self):
		Entity.draw(self)
		sys.stdout.write(self._message + " ({})\n".format(self._counter))