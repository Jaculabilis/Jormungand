import sys
from random import randrange

class Entity(object):
	"""
	An Entity is something that exists in the Fishtank entities list. The Entity class provides
	some basic structure to the behavior of entities, including position and velocity,
	serialization, and update and draw. Each entity has a random 8-digit hex id for identification
	purposes.
	"""
	def __init__(self):
		self.fishtank = None
		self.id = randrange(16**8)
		self.x = 0
		self.y = 0
		self.z = 0
		self.vx = 0
		self.vy = 0
	
	def __repr__(self):
		return "[{}#{:8x} p{},{} z{} v{},{}]".format(type(self).__name__,
			self.id, self.x, self.y, self.z, self.vx, self.vy)
	
	def __str__(self):
		return "[{}#{:8x}]".format(type(self).__name__, self.id)

	def serialize(self):
		"""
		Returns a JSON-compatbible representation of the current state of this entity.
		Subclasses should override this method, call it from their superclass, then update the
		returned representation with its own information, including the subclass's module and
		class and any idiomatic fields of that class.
		Output:	serialized representation of this entity
		"""
		return {
			"module":"entity.Entity",
			"class":"Entity",
			"id":"{:8x}".format(self.id),
			"p":[self.x,self.y],
			"z":self.z,
			"v":[self.vx,self.vy]
		}
	
	@staticmethod
	def deserialize(serial):
		"""
		Reconstructs an Entity from a serialized representation as returned by Entity.serialize().
		Subclasses should reimplement this method with e as their own class.
		Input:	serial, a serialized representation of an entity
		Output:	an entity reproducing the state represented in serial
		"""
		e = Entity()
		return Entity.rebuild(e, serial)
	
	@staticmethod
	def rebuild(e, serial):
		"""
		Helper function for Entity.deserialize().
		Subclasses should override this method, call it from their superclass, then add
		deserialization for their idiomatic fields.
		Input:	e, a newly initialized entity
				serial, a serialized representation of an entity as passed to deserialize()
		Output:	an entity reproducing the state represented in serial
		"""
		e.id = int(serial['id'], 16)
		e.x, e.y = serial['p']
		e.z = serial['z']
		e.vx, e.vy = serial['v']
		return e
	
	def update(self, delta):
		"""
		Updates this entity during the update pass of the game loop.
		Input:	delta, the number of seconds since the last tick
		"""
		pass
	
	def draw(self, screen):
		"""
		Draws this entity during the draw pass of the game loop.
		Input: screen, a Surface object to draw this entity on.
		"""
		pass