import sys
from entity.Entity import Entity
from entity.Tube import Tube

class DebugJumper(Entity):
	def __init__(self, message):
		Entity.__init__(self)
		self.message = message
		self.counter = 0
	
	def __repr__(self):
		return "[DebugJumper @{},{} message='{}' counter={}]".format(self.x, self.y, self.message, self.counter)
	
	def serialize(self):
		sup = Entity.serialize(self)
		sup.update({
			"module":"entity.dummy.DebugJumper",
			"class":"DebugJumper",
			"message":self.message,
			"counter":self.counter
		})
		return sup
	
	@staticmethod
	def deserialize(serial):
		e = DebugJumper(serial["message"])
		e.counter = serial["counter"]
		return e
	
	def update(self, delta):
		Entity.update(self)
		self.counter += 1
		if self.counter % 5 == 0:
			for entity in self.fishtank.entities:
				if type(entity) is Tube:
					entity.accept(self)
					break
	
	def draw(self, screen):
		Entity.draw(self)
		sys.stdout.write(self.message + " ({})\n".format(self.counter))