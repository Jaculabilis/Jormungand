import sys
import time
import json

class Fishtank():
	def __init__(self, recv_queue):
		self._entities = []
		self._to_remove = []
		self._recv_queue = recv_queue
	
	def run(self):
		while True:
			# Delete flagged entities
			if self._to_remove:
				for entity in self._to_remove:
					self._entities.remove(entity)
				self._to_remove = []
			# Update and draw
			for entity in self._entities:
				entity.update()
			for entity in self._entities:
				entity.draw()
			#time.sleep(1)
			# Intake queue
			if not self._recv_queue.empty():
				serial = self._recv_queue.get(False)
				sys.stdout.write("Fishtank dequeued a {}\n".format(serial["class"]))
				mod = __import__(serial["module"], fromlist=[serial["class"]])
				klass = getattr(mod, serial["class"])
				e = klass.deserialize(serial)
				self.add_entity(e)
	
	def add_entity(self, entity):
		entity._fishtank = self
		self._entities.append(entity)
		sys.stdout.write("Added: {}\n".format(repr(entity)))
	
	def remove_entity(self, entity):
		if entity not in self._entities:
			sys.stderr.write(
				"WARN: remove called for entity '{}', but it isn't in the eneityt list\n".format(entity.__name__))
			return
		self._to_remove.append(entity)