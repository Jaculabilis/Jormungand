import sys
from entity.Entity import Entity
from util.Util import logout, load_image

class Tube(Entity):
	def __init__(self, network_gate):
		Entity.__init__(self)
		self.gate = network_gate
		self.inbox = []
		self.texture = load_image("tube.png")
		self.x, self.y = 200, 200
		self.z = -1
	
	def __repr__(self):
		return "[Tube gate={} inbox={}]".format(repr(self.gate), repr(self.inbox))
	
	def accept(self, entity):
		self.fishtank.remove_entity(entity)
		self.inbox.append(entity)
		logout("Accepted: {}".format(str(entity), "Tube#{}".format(self.id)))
	
	def update(self, delta):
		Entity.update(self, delta)
		if self.inbox:
			entity = self.inbox.pop(0)
			self.gate.transmit(entity.serialize())
	
	def draw(self, screen):
		Entity.draw(self, screen)
		rect = self.texture.get_rect()
		rect.center = (int(self.x), int(self.y))
		screen.blit(self.texture, rect)