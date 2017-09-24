import sys
from entity.Entity import Entity

class DebugWaiter(Entity):
	def __init__(self, message):
		Entity.__init__(self)
		self._message = message
		self._counter = 0
	
	def __repr__(self):
		return "[DebugWaiter message='{}' counter={}]".format(self._message, self._counter)
	
	def update(self):
		Entity.update(self)
		self._counter += 1
	
	def draw(self):
		Entity.draw(self)
		sys.stdout.write(self._message + " ({})\n".format(self._counter))