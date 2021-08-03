import pygame
import numpy
import random
class actor:
	def __init__(self, x=0, y=0, w=0, h=0, Θ=0,hitboxes=0,index= 0,name = None,predict = False,room=0):
		self.hitboxes = hitboxes
		self.isjump = False
		self.predict = predict
		self.name = name
		self.x = x
		self.y = y
		self.vx = 0
		self.vy = 0
		self.w = w
		self.h = h
		self.Θ = Θ
		self.index = index 
		self.id = 0
		self.room = 0
		numbs = []
		for word in self.index:
			if word.isdigit():
				numbs.append(int(word))
		number = (sum(numbs) / len(numbs))*40
		img_surface = pygame.image.load(r'playerm.png')
		
		img_array = pygame.surfarray.array3d(img_surface)         # Convert it into an 3D array
		colored_img = numpy.array(img_array)                      # Array thing
		colored_img[:, :, 0] = 10*number   # <-- Red
		colored_img[:, :, 1] = 20*number # <-- Green
		colored_img[:, :, 2] = 30*number    # <-- Blue
		img_surface = pygame.surfarray.make_surface(colored_img)
		self.image = img_surface

	def physicsHandler(self,timedelta):
		# gravity
		g = 1.38
		#wall collision
		if self.inBounds(self.x+self.vx*(timedelta/10), self.y) == False:
			self.x += self.vx*(timedelta/10)
		else:
			self.vx = 0
		#friction
		if self.vx is not 0:
			self.vx *= 0.90
		#gravity/falling/floor collisons
		if self.inBounds(self.x, self.y+g+self.vy) == False:
			self.vy += g
			self.y += self.vy 
		else:
			self.vy += g
			self.vy *= 0.25 *(timedelta/10)
			if self.inBounds(self.x,self.y+g+self.vy) == True:
				self.isjump = False
				self.vy = 0


		

	def inBounds(self, x, y):
			for hitbox in self.hitboxes:
				if (hitbox.x) < (x+self.w) and hitbox.x + hitbox.w > x:
					if hitbox.y + hitbox.h> y and hitbox.y < (y+self.h):
						return True	
			return False

	def render(self, screen):
		buttonfont = pygame.font.Font(r"arial.ttf", 25)

		rects = pygame.Rect((self.x, self.y), (self.w, self.h))
		rotated = pygame.transform.rotate(self.image,0)
		rotatedrect = rotated.get_rect(center=rects.center)
		textSurf = buttonfont.render(self.name, 1, (255,255,255))
		textRect = textSurf.get_rect()
		textRect.center = ((self.x+10, self.y-20))
		screen.blit(textSurf, textRect)
		
		screen.blit(self.image, rects)
		

	def setPos(self, x, y):

		self.x = x
		self.y = y

	def setRoom(self, room):

		self.room = room

	def setVx(self,x):
		if self.inBounds(self.x , self.y) == False:
			self.vx = x

	def setVy(self,y):
		if self.inBounds(self.x , self.y) == False:
			self.vy = y

	def jump(self):
		if self.inBounds(self.x, self.y) == False:
			if self.isjump == False and self.vy == 0:
				self.vy += -25
				self.isjump = True

	def moveUp(self):
		if self.inBounds(self.x, self.y) == False:
			if self.isjump == False and self.vy == 0:
				self.vy += -25
				self.isjump = True
				

	def moveLeft(self):
		if self.inBounds(self.x , self.y) == False:
			self.vx -= 0.92


	def moveRight(self):
		if self.inBounds(self.x, self.y) == False:
			self.vx += 0.92


	def setAngle(self, Θ=0):
			self.Θ = Θ
