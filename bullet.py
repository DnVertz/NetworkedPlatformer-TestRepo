import pygame
import numpy
import random
class bullet:
	def __init__(self,position = 0,speed = 0,idd = 0,room = 0):
		self.position = position
		self.speed = speed
		self.room = room
		self.idd = idd

	def setPos(self, x, y):

		self.x = x
		self.y = y

	def inBounds(self, x, y):
			for hitbox in self.hitboxes:
				if (hitbox.x) < (x+self.w) and hitbox.x + hitbox.w > x:
					if hitbox.y + hitbox.h> y and hitbox.y < (y+self.h):
						return True	
			return False

