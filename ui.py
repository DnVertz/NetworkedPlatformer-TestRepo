import pygame
#import Slider
#from pygame_widgets import Button
#used when rendering the complex buttons in menus
class uistate:
	def __init__(self):
		self.state = ""
		self.blur = 6
	def setState(self, state2):
		self.state = state2
	def setBlur(self, blur):
		self.blur = blur

class button():
	def __init__(self, text, x=0, y=0, w=0, h=0, activeColour=(153,0,0), defaultColour=(41,41,41)):
		self.text = text
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.activeColour = activeColour
		self.defaultColour = defaultColour
		self.colour = defaultColour

	def render(self, screen):
		mouseX, mouseY = pygame.mouse.get_pos()
		image = pygame.Surface([self.w, self.h])
		if self.x + self.w > mouseX > self.x and self.y + self.h > mouseY > self.y:
			self.colour = self.activeColour
			pygame.draw.rect(screen, self.defaultColour, (self.x-10,self.y-10,self.w+20,self.h+20))
		else:
			self.colour = self.defaultColour

			
		pygame.draw.rect(screen, self.colour, (self.x,self.y,self.w,self.h))
		buttonfont = pygame.font.Font(r"arial.ttf", 25)
		textSurf = buttonfont.render(self.text, 1, (255,255,255))
		textRect = textSurf.get_rect()
		textRect.center = ((self.x+(self.w/2)), (self.y+(self.h/2)))
		screen.blit(textSurf, textRect)
	
	def pressed(self,events):
		mouseX, mouseY = pygame.mouse.get_pos()
		if self.x + self.w > mouseX > self.x and self.y + self.h > mouseY > self.y:
			for event in events:
				if event.type == pygame.MOUSEBUTTONDOWN:
					return True
class textbutton():
	def __init__(self, text, x=0, y=0, w=0, h=0,number= True,activeColour=(153,0,0), defaultColour=(41,41,41)):
		self.text = text
		self.text2 = ''
		self.x = x
		self.number = number
		self.y = y
		self.w = w
		self.h = h
		self.clock = 0
		self.pointer = " "
		self.lst = []
		self.activeColour = activeColour
		self.defaultColour = defaultColour
		self.colour = defaultColour


	def render(self, screen,events):
		mouseX, mouseY = pygame.mouse.get_pos()
		image = pygame.Surface([self.w, self.h])
		if self.x + self.w > mouseX > self.x and self.y + self.h > mouseY > self.y:
			self.clock += 2
			self.colour = self.activeColour
			pygame.draw.rect(screen, self.defaultColour, (self.x-10,self.y-10,self.w+20,self.h+20))
			self.lst = []

			for event in events:
				if event.type == pygame.KEYDOWN:
					if pygame.key.name(event.key) != 'backspace' and pygame.key.name(event.key) != 'space' and pygame.key.name(event.key):
						if self.number == False and len(self.text2) > 6:
							self.text2 = self.text2[:-1]
							if len(self.lst) > 0:
								del self.lst[len(self.lst)-1]

						if self.number == True and len(self.text2) > 16:
							self.text2 = self.text2[:-1]
							if len(self.lst) > 0:
								del self.lst[len(self.lst)-1]


						elif pygame.key.name(event.key).isnumeric() == True or pygame.key.name(event.key) == "." or (len(pygame.key.name(event.key)) == 1):
							self.lst.append(pygame.key.name(event.key))
						


					#elif pygame.key.name(event.key) == "space" and self.n:
						#self.lst.append(" ")

					else:
						self.text2 = self.text2[:-1]
						if len(self.lst) > 0:

							del self.lst[len(self.lst)-1]
				
			for x in self.lst:
					self.text2 += x

		else:
			self.clock = 0
			self.pointer = " "
			self.colour = self.defaultColour

			
		pygame.draw.rect(screen, self.colour, (self.x,self.y,self.w,self.h))
		buttonfont = pygame.font.Font(r"arial.ttf", 25)

		if self.text2 is not '':
			textSurf = buttonfont.render(self.text + self.text2 +self.pointer, 1, (255,255,255))
		else:
			textSurf = buttonfont.render(self.text+self.pointer, 1, (255,255,255))

		textRect = textSurf.get_rect()
		textRect.center = ((self.x+(self.w/2)), (self.y+(self.h/2)))
		screen.blit(textSurf, textRect)

		if self.clock == 2:
			self.pointer = "|"

		if self.clock == 50:
			self.pointer = " "

		if self.clock == 102:
			self.clock = 0

		return self.text2
	
	def pressed(self,events):
		mouseX, mouseY = pygame.mouse.get_pos()
		if self.x + self.w > mouseX > self.x and self.y + self.h > mouseY > self.y:
			for event in events:
				if event.type == pygame.MOUSEBUTTONDOWN:
					return self.text2 

class textbutton2():
	def __init__(self, text, x=0, y=0, w=0, h=0,activeColour=(153,0,0), defaultColour=(41,41,41)):
		self.text = text
		self.text2 = ''
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.clock = 0
		self.pointer = " "
		self.lst = []
		self.activeColour = activeColour
		self.defaultColour = defaultColour
		self.colour = defaultColour


	def render(self, screen,events):
		mouseX, mouseY = pygame.mouse.get_pos()
		image = pygame.Surface([self.w, self.h])
		if self.x + self.w > mouseX > self.x and self.y + self.h > mouseY > self.y:
			self.clock += 2
			self.colour = self.activeColour
			pygame.draw.rect(screen, self.defaultColour, (self.x-10,self.y-10,self.w+20,self.h+20))
			self.lst = []

			for event in events:
				if event.type == pygame.KEYDOWN:
					if pygame.key.name(event.key) != 'backspace' and pygame.key.name(event.key) != 'space' and pygame.key.name(event.key) != 'return' and pygame.key.name(event.key) and len(self.text2) < 30 and len(pygame.key.name(event.key)) == 1:
						self.lst.append(pygame.key.name(event.key))

					elif pygame.key.name(event.key) == "space":
						self.lst.append(" ")

					elif pygame.key.name(event.key) == "return":
						
						self.lst = []
						rturn = self.text2
						self.text2 = ''
						return rturn



					elif  pygame.key.name(event.key) == "backspace":
						self.text2 = self.text2[:-1]
						if len(self.lst) > 0:

							del self.lst[len(self.lst)-1]
				
			for x in self.lst:
					self.text2 += x

		else:
			self.clock = 0
			self.pointer = " "
			self.colour = self.defaultColour

			
		pygame.draw.rect(screen, self.colour, (self.x,self.y,self.w,self.h))
		buttonfont = pygame.font.Font(r"arial.ttf", 25)

		if self.text2 is not '':
			textSurf = buttonfont.render(self.text + self.text2 +self.pointer, 1, (255,255,255))
		else:
			textSurf = buttonfont.render(self.text+self.pointer, 1, (255,255,255))

		textRect = textSurf.get_rect()
		textRect.center = ((self.x+(self.w/2)), (self.y+(self.h/2)))
		screen.blit(textSurf, textRect)

		if self.clock == 2:
			self.pointer = "|"

		if self.clock == 50:
			self.pointer = " "

		if self.clock == 102:
			self.clock = 0

		#return self.text2
	
	def pressed(self,events):
		mouseX, mouseY = pygame.mouse.get_pos()
		if self.x + self.w > mouseX > self.x and self.y + self.h > mouseY > self.y:
			for event in events:
				if event.type == pygame.MOUSEBUTTONDOWN:
					return self.text2 







		
			

					






