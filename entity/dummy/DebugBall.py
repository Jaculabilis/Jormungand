import sys
import random
import pygame
from entity.Entity import Entity
from entity.Tube import Tube
from util.Util import load_image

class DebugBall(Entity):
	"""
	A debug entity that bounces around and jumps through network tubes.
	"""
	def __init__(self):
		Entity.__init__(self)
		self.vx = 32
		self.vy = 128
		self.dummy = "DUMMY"
		self.texture = load_image("ball64.png")
		self.texture = pygame.transform.smoothscale(self.texture, (16,16))
		self.rect = pygame.Rect(0, 0, 16, 16)
	
	def serialize(self):
		e = Entity.serialize(self)
		e.update({
			"module":"entity.dummy.DebugBall",
			"class":"DebugBall",
			"dummy":self.dummy
		})
		return e
	
	@staticmethod
	def deserialize(serial):
		e = DebugBall()
		return DebugBall.rebuild(e, serial)
	
	@staticmethod
	def rebuild(e, serial):
		Entity.rebuild(e, serial)
		e.dummy = serial["dummy"]
		return e
	
	def update(self, delta):
		Entity.update(self, delta)
		self.x += self.vx * delta
		self.y += self.vy * delta
		if self.x < 0 or self.x > self.fishtank.size[0]:
			self.vx = -self.vx
			self.x = 0 if self.x < 0 else self.fishtank.size[0] if self.x > self.fishtank.size[0] else self.x
		if self.y < 0 or self.y > self.fishtank.size[1]:
			self.vy = -self.vy
			self.y = 0 if self.y < 0 else self.fishtank.size[1] if self.y > self.fishtank.size[1] else self.y
		
		for entity in self.fishtank.entities:
			if type(entity) is Tube and abs(self.x - entity.x) < 64 and abs(self.y - entity.y) < 64:
				entity.accept(self)
				break
	
	def draw(self, screen):
		Entity.draw(self, screen)
		#rect = self.texture.get_rect()
		self.rect.center = (int(self.x), int(self.y))
		screen.blit(self.texture, self.rect)
		