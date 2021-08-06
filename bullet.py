import pygame
import numpy
import random
class bullet:
	def __init__(self,position = 0,speed = 0,idd = 0,room = 0,size = 0):
		self.position = position
		self.speed = speed
		self.room = room
		self.idd = idd
		self.size = size

	def setPos(self, x, y):

		self.x = x
		self.y = y
			

