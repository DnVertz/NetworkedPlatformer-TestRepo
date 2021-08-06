import pygame
import numpy
import random
import bullet
#import uuid
import socket
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
		self.bulletsize = 2
		self.w = w
		self.h = h
		self.Θ = Θ
		self.spread = 10
		self.index = index 
		self.id = 0
		self.room = 0
		self.ammo = 0
		self.maxammo = 10
		self.reloadtime = 50
		self.reloadprog = 0
		self.reloading = False
		self.all_bullets = []
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
		if self.vx is not 0 and self.vy == 0:
			self.vx *= 0.75
		elif self.vy is not 0:
			self.vx *= 0.95

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
		if self.reloading == True:
			self.reloadprog += 1

			if self.reloadprog > self.reloadtime:
				self.reloading = False
				self.ammo = 0

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
			if self.vy == 0:
				self.vx -= 1.75
			else:
				self.vx -= 0.5



	def moveRight(self):
		if self.inBounds(self.x, self.y) == False:
			if self.vy == 0:
				self.vx += 1.75
			else:
				self.vx += 0.5



	def setAngle(self, Θ=0):
			self.Θ = Θ

	def reload(self):
			self.ammo = 0
			self.reloadprog = 0
	def weapon_one(self):
			self.ammo = 0
			self.maxammo = 10
			self.spread = 10
			self.bulletsize = 2
			self.reloadtime = 50

	def weapon_two(self):
			self.ammo = 0
			self.maxammo = 5
			self.spread = 2
			self.bulletsize = 5
			self.reloadtime = 70

	def weapon_three(self):
			#write in thing that caches weapon ammo
			self.ammo = 0
			self.maxammo = 2
			self.spread = 20
			self.bulletsize = 10
			self.reloadtime = 30

	def reload(self):
			self.reloadprog = 0
			self.reloading = True
			

	def shoot(self,sock,server,clientid,deathtimeout):
		if deathtimeout > 100:
			if self.reloading == False:
				SPEED = 20
				start = pygame.math.Vector2(self.x,self.y)
				mouse = pygame.mouse.get_pos()
				distance = mouse - start
				positions = pygame.math.Vector2(start) 
				speed = distance.normalize() * SPEED
				newbullet = bullet.bullet(positions,speed)
				newbullet.room = self.room
				newbullet.idd = clientid
				newbullet.size = self.bulletsize
				if self.ammo < self.maxammo:
					self.ammo += 1
					#self.all_bullets.append(newbullet)
					data2 = "joinbullet;"+str(newbullet.position.x)+";"+str(newbullet.position.y+random.randint(-int(self.spread),int(self.spread)))+";"+str(newbullet.speed.x)+";"+str(newbullet.speed.y)+";"+str(newbullet.idd)+";"+str(newbullet.room)+";"+str(newbullet.size)+"\n"
					data2 = data2.encode('UTF-8')
					sock.sendto(data2,server)
		#return(all_bullets)

	def remove(self,position,speed):
		self.all_bullets.remove([position, speed])
