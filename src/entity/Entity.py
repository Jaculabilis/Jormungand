import sys

class Entity(object):
	def __init__(self):
		pass
	
	def __repr__(self):
		return "[Entity]"

	def serialize(self):
		return {
			"module":"entity.Entity",
			"class":"Entity"
		}
	
	@staticmethod
	def deserialize(serial):
		e = Entity()
		return e
	
	def update(self):
		pass
	
	def draw(self):
		pass