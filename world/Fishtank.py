import sys
import time
import json
import pygame
from util.Util import logout, logerr

class Fishtank():
	def __init__(self, recv_queue):
		self.entities = []
		self.to_remove = []
		self.recv_queue = recv_queue
		
		self.size = (480, 360)
		self.screen = pygame.display.set_mode(self.size)
	
	def run(self):
		"""Begins the game loop. Does not return."""
		clock = pygame.time.Clock()
		
		while True:
			# Upkeep
			milli = clock.tick(60) / 1000
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
		
			# Delete flagged entities
			if self.to_remove:
				for entity in self.to_remove:
					self.entities.remove(entity)
				self.to_remove = []
			
			# Update
			for entity in self.entities:
				entity.update(milli)
			
			# Intake queue
			if not self.recv_queue.empty():
				serial = self.recv_queue.get(False)
				logout("Dequeued: {}".format(serial["class"]), "Fishtank")
				mod = __import__(serial["module"], fromlist=[serial["class"]])
				klass = getattr(mod, serial["class"])
				e = klass.deserialize(serial)
				self.add_entity(e)
			
			# Draw
			self.screen.fill((100, 149, 237))
			for entity in sorted(self.entities, key=lambda e:e.z):
				entity.draw(self.screen)
			pygame.display.flip()
	
	def add_entity(self, entity):
		"""
		Adds an entity to the entity list and sets its fishtank property to this.
		Input:	entity, the entity to add
		"""
		entity.fishtank = self
		self.entities.append(entity)
		logout("Added: {}".format(repr(entity)), "Fishtank")
	
	def remove_entity(self, entity):
		"""
		Marks an entity to be removed before the next update pass.
		Input:	entity, the entity to remove
		"""
		if entity not in self.entities:
			logerr("WARN: remove called for entity '{}',"\
					"but it isn't in the entity list".format(entity.__name__), "Fishtank")
			return
		self.to_remove.append(entity)