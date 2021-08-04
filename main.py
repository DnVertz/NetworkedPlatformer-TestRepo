from threading import Thread
import pygame 
import ui
import menu
#import player
import inputs
import hitboxes
import actor
import random
import socket
import os
import signal
import sys
import bullet
import pygame.freetype
all_bullets = []

HOST = None
PORT = None
lockout = False
kicked = False
state = ui.uistate()
width = 1024
height = 640
quitol = False
clientid = 1
title = "Platformer"
player1 = None
predict = False
msgbox = False
name = None
msgtimeout = 0
deathmsgtimeout = 0

screen = pygame.display.set_mode((width, height),pygame.SCALED,vsync = 1 )
#corner(x,y),(width,height)
#,[(500,10),(1,500)]

coll = [(0,0),(0,640)],[(1024,0),(1024,640)],[(0,640),(1024,640)],[(0,0),(1024,0)],[(0,500),(300,500)],[(500,450),(60,125)],[(800,400),(500,400)]
coll0 = [(0,0),(0,640)],[(1024,0),(1024,640)],[(0,640),(1024,640)],[(0,0),(1024,0)],[(0,500),(300,500)],[(500,450),(60,125)],[(800,400),(500,400)]
coll1 = [(0,0),(0,640)],[(1024,0),(1024,640)],[(0,640),(1024,640)],[(0,0),(1024,0)],[(0,500),(200,500)],[(500,450),(60,125)],[(800,400),(500,400)]
#stores the level hitboxes... can and will be changed into a text file
hitbox = []#loads the hitboxes
multiplays = []#stores the actor class
messages = []
deathmessages = []
for x in coll:
	hitbox.append(hitboxes.hitboxes(x[0][0],x[0][1],x[1][0],x[1][1]))

state.state = "start"
pygame.init()
titlefont = pygame.font.Font(r'arial.ttf', 40)
titlefont2 = pygame.font.Font(r'arial.ttf', 30)
messagefont = pygame.font.Font(r'arial.ttf', 20)

while True:
	if quitol == True:
		break
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			os._exit(1)

	if state.state == "start":
		screen.fill((128,128,128))
		start = menu.drawStart(screen, titlefont, state,events,title)
		if start is not None:
			connec = start
			state.state = "joincheck"
	else:
		try: 
			sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
			server_address = (str(connec[0]), int(connec[1]))
			name = str(connec[2])
			
			msgs = str("join;"+name+"\n")
			byte = msgs.encode()
			sock.sendto(byte,server_address)
			sock.settimeout(0.5)
			initdata2,addr = sock.recvfrom(4096)
			initdata2 = initdata2.decode('UTF-8')
			print(initdata2)

			if initdata2 == "True":
				break
			else:
				title = "Name in use!!!!"
				state.state = "start"

		except:
			title = "Wrong IP/Port!!!!"
			state.state = "start"

	pygame.display.flip()

print("hello?")
sock.settimeout(None)
initdata,addr = sock.recvfrom(4096)

initdata = initdata.decode('UTF-8')
split = initdata.split("\n")
for p in split:
	split2 = p.split(";")
	if split2[0] == "init":
		clientid = split2[1]
		multiplays.append(actor.actor(int(split2[2]), int(split2[3]),25 ,50 ,0,hitbox,split2[1],split2[4]))
		player1 = actor.actor(int(split2[2]), int(split2[3]),25 ,50 ,0,hitbox,split2[1],split2[4])



clock = pygame.time.Clock() 
FPS = 60
fps = clock.tick(FPS)

def networkthread(clientid):
	global predict
	global messages
	global msgtimeout
	global kicked
	global player1
	#print("yes")
	while True:
		try:
			data,addr2 = sock.recvfrom(4096)
		except:
			break

		data = data.decode('UTF-8')
		split = data.split("\n")

		for p in split:
			split2 = p.split(";")

			if split2[0] == "spawn":

				if split2[1] is not clientid:
					multiplays.append(actor.actor(int(split2[2]), int(split2[3]),25 ,50 ,0,hitbox,split2[1],split2[4]))

			if split2[0] == "join":
				if split2[1] is not clientid:
					multiplays.append(actor.actor(int(split2[2]), int(split2[3]),25 ,50 ,0,hitbox,split2[1]))

			if split2[0] == "pos":
					for x in multiplays:
						if x.index == split2[1]:
							x.setPos(int(split2[2]),int(split2[3]))
							print(split2[4])
							x.setRoom(split2[4])

			if split2[0] == "leave":
				print("x")
				if split2[1] == clientid:
					os._exit(1)
				for x in multiplays:
					if x.index == split2[1]:
						multiplays.remove(x)

			if split2[0] == "msg":
				messages.append(split2[1]+": "+split2[2])
				msgtimeout = 0

			if split2[0] == "bspawn":
				newbul = bullet.bullet(pygame.math.Vector2(int(float(split2[1])),int(float(split2[2]))),pygame.math.Vector2(int(float(split2[3])),int(float(split2[4]))))
				print(split2[1])
				newbul.idd = split2[3]
				player1.all_bullets.append(newbul)





			if split2[0] == "die":
				messages.append(split2[1] +" has died")
				msgtimeout = 0

	os._exit(1)

thr = Thread(target = networkthread,args =(str(clientid),))
thr.start()

def signal_handler(sig, frame):
	print('You pressed Ctrl+C!')
	data2 = "leave;"+str(clientid)+"\n"
	data2 = data2.encode('UTF-8')
	sock.sendto(data2,server_address)
	os._exit(1)

def roomcheck(player1):

	global lockout
	if player1.x > 995:
		if player1.room < 1:
			player1.room += 1
			player1.x = 4
			player1.y = 0
			lockout = True
			print(lockout)
			player1.vx = 0
			
	elif player1.x < 3:
		if player1.room > 0:
			player1.room -= 1
			player1.x = 993
			player1.y = 0
			lockout = True
			print(lockout)
			player1.vx = 0

	if player1.y > 560:
		player1.room = 0
		player1.x = 4
		player1.y = 0
		lockout = True
		print(lockout)
		player1.vx = 0
		data2 = "die;"+str(player1.name)+"\n"
		data2 = data2.encode('UTF-8')
		sock.sendto(data2,server_address)

			
			







while True:

	signal.signal(signal.SIGINT, signal_handler)
	roomcheck(player1)

	screen.fill((128,128,128))
	roomsg = "Room: "+str(player1.room +1)
	lenofmsg = titlefont2.size(roomsg)


	if player1.all_bullets is not None:
		#Check if bullets have collided 
		for z in player1.all_bullets :
			z.position += z.speed
			pos_x = int(z.position.x)
			pos_y = int(z.position.y)


			pygame.draw.rect(screen, (255,255,255), (pos_x, pos_y,10,10))
			if not 0<z.position.x < 1000:
				if not 640 <z.position.y <0: 
					player1.all_bullets.remove(z)

	char1 = titlefont2.render("Room: "+str(player1.room +1), 1, (255,255,255))
	screen.blit(char1, (1024-lenofmsg[0] , 10))

	coll = eval("coll" + str(player1.room))
	hitbox = []

	for x in coll:
		hitbox.append(hitboxes.hitboxes(x[0][0],x[0][1],x[1][0],x[1][1]))
	player1.hitboxes = hitbox

	if quitol == True:
		data2 = "leave;"+str(clientid)+"\n"
		data2 = data2.encode('UTF-8')
		sock.sendto(data2,server_address)
		break
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			quitol = True
	for x in coll:
		if coll.index(x) >= 4:
			pygame.draw.rect(screen,(60,60,60),(x[0][0],x[0][1],x[1][0],x[1][1]))



	
	if player1 is not None:

		player1.physicsHandler(fps)
		data2 = "pos;"+str(clientid)+";"+str(int(player1.x))+";"+str(int(player1.y))+";"+str(int(player1.room))+"\n"
		data2 = data2.encode('UTF-8')
		sock.sendto(data2,server_address)
		if len(messages) > 0:
			msgtimeout += 1

		if len(messages) == 7 or (msgtimeout > 350 and len(messages)>0):
			msgtimeout = 0
			messages.remove(messages[0])


		


		player1.render(screen)

		for p in multiplays:
			if p.index != clientid:
				
				if int(p.room) == int(player1.room):
					p.render(screen)

		for i in range(len(messages)):
			amount = messagefont.size(messages[i])
			lst = messages[i].split()
			lst2 = list(lst[0])
			print(lst2)
			if ":" not in lst2:
				message = lst[0]+" "+lst[1]+" "
				message2 = lst[2]
				font = pygame.freetype.Font(None, 50)
				amount2 = messagefont.size(message)
				
				textSurf = messagefont.render(message, 1, (255,255,255))
				textRect = pygame.Rect(0+5,i*40, amount[0], amount[1])
				textSurf2 = messagefont.render(message2, 1, (255,0,0) )
				textRect2 = pygame.Rect((0+5+amount2[0]),i*40, amount[0], amount[1])
				screen.blit(textSurf, textRect)
				screen.blit(textSurf2, textRect2)


			else:
				textSurf = messagefont.render(messages[i], 1, (255,255,255))
				textRect = pygame.Rect(0+5,i*40, amount[0], amount[1])
				#textRect.center = (((100/2)), (60+(60/2)+i*40))
				#textRect.center = (0+amount[0],0+amount[1]+i*40)
				screen.blit(textSurf, textRect)

				


		if msgbox == True:
			start = menu.drawMessage(screen, state,events,title)
			if start != None and start != '' and start != ' ':
				connec = start
				data2 = "msg;"+str(connec)+";"+str(name)+"\n"
				data2 = data2.encode('UTF-8')
				sock.sendto(data2,server_address)

		#if kicked == True:
		if lockout == False:
			x = inputs.run(state,player1,events,msgbox,sock,server_address)

		if lockout == True:
			if player1.vy == 0:
				lockout = False
		if x == True:
			if msgbox == True:
				msgbox = False 
			else:
				msgbox = True


			
		


		pygame.display.flip()




sock.close()
