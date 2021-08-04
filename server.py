from threading import Thread
from threading import Lock
import time


import uuid, asyncio
import socket
import socketserver
#Jank cannot describe this solution
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.connect(("8.8.8.8", 8008))
HOSTname = str(s.getsockname()[0])
s.close()
PORT = 8008
HOST = ''
players = []
#players_lock = threading.Lock()
s_print_lock = Lock()
def s_print(*a, **b):
    """Thread safe print function"""
    with s_print_lock:
        print(*a, **b)


def broadcast(data):
	for player in players:
		try:
			player.socket.write(data)
		except:
			pass

def removePlayer(playerID):
	for player in players:
		if player.id == playerID:
			players.remove(player)

def sendPlayerInit(player, addr,socket):
	data = "init;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+";"+str(player.name)+"\n"
	socket.sendto(data.encode('UTF-8'),addr)


def sendPlayerSpawn(player,addr):
	data = "spawn;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+";"+str(player.name)+"\n"
	player.socket.sendto(data.encode('UTF-8'),addr)

def sendPlayerJoin(player):
	data = "join;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+"\n"
	broadcast(data.encode('UTF-8'))

def sendPlayerLeave(player,addr,socket):
	data = "leave;"+str(player.id)+"\n"
	socket.sendto(data.encode('UTF-8'),addr)

def sendPlayerPos(player,addr):
	data = "pos;"+str(player.id)+";"+str(int(player.x))+";"+str(int(player.y))+";"+str(int(player.room))+"\n"
	player.socket.sendto(data.encode('UTF-8'),addr)

def sendPlayerMsg(socket,message,addr,name):
	data = "msg;"+str(name)+";"+str(message)+"\n"
	socket.sendto(data.encode('UTF-8'),addr)

def sendPlayerDie(socket,addr,id):
	data = "die;"+str(id)+"\n"
	socket.sendto(data.encode('UTF-8'),addr)

def sendPlayerTest(socket,addr):
	data = "test;"+"\n"
	socket.sendto(data.encode('UTF-8'),addr)

def timeout():
	while True:
		global players
		try:
			for i in range(len(players)):
				print(players[i].timeout)
				if players[i].timeout == 60: 
					for p in players:
						sendPlayerLeave(players[i],p.addr,p.socket)
					players.remove(players[i])
					break
				else:
					
					pos = (players[i].x,players[i].y)
					time.sleep(1)
					pos2 = (players[i].x,players[i].y)
					if pos == pos2:
						players[i].timeout += 1
					else:
						players[i].timeout = 0

				
		except:
			pass



thr = Thread(target = timeout,args =())
#thr.start()

class PositionUpdate:
	def __init__(self, pid, x: int, y: int):
		self.id = pid
		self.x = x
		self.y = y
	def updatePlayer(self):
		for i in range(len(players)):
			if players[i].id == self.id:
				players[i].x = self.x
				players[i].y = self.y
				break
	def forwardToClients(self):
		data = "pos;"+str(self.id)+";"+str(self.x)+";"+str(self.y)+"\n"
		broadcast(data.encode('UTF-8'))



class Player:
	def __init__(self, socket,addr,name):
		self.id = uuid.uuid1()
		self.socket = socket
		self.addr = addr
		self.name = name
		self.x = 0
		self.y = 0
		self.vx = 0
		self.vy = 0
		self.timeout = 0
		self.room = 0
	def setPosition(self, x, y):
		self.x = x
		self.y = y
	def getPosition(self):
		return (self.x, self.y)



class MyUDPHandler(socketserver.DatagramRequestHandler):
	def handle(self):
		#print("a")
		data = self.request[0].strip()
		socket = self.request[1]
		#socket.settimeout(10)
		data = data.decode()
		#print(self.request)
		split = data.split(";")



		if split[0] == 'join':
			allow = True
			for x in players:
				if x.name == split[1]:
					msg = "False"
					msg = msg.encode()
					allow = False
					socket.sendto(msg,self.client_address)

			if allow == True:
				msg = "True"
				msg = msg.encode()
				socket.sendto(msg,self.client_address)
				player = Player(socket,self.client_address,split[1])
				playerID = player.id
				players.append(player)
				sendPlayerInit(player, self.client_address,socket) #send init id and pos to player
				for p in players:
					#print(p.id)
					if p is not player:
						sendPlayerSpawn(p,player.addr)
						sendPlayerSpawn(player,p.addr)
					else:		
						sendPlayerSpawn(player,p.addr)
		
		elif split[0] == 'pos':
			for i in range(len(players)):
				if str(players[i].id) == split[1]:
					players[i].x = split[2]
					players[i].y = split[3]
					players[i].room = split[4]
					for p in players:
						if str(p.id) != str(players[i].id):
							sendPlayerPos(players[i],p.addr)
							
		elif split[0] == 'leave':
			for i in range(len(players)):
				if str(players[i].id) == split[1]:
					for p in players:
						if str(p.id) != str(players[i].id):
							sendPlayerLeave(players[i],p.addr,socket)
					players.remove(players[i])
						
					break
		elif split[0] == 'msg':
			for p in players:
				p.timeout = 0
				sendPlayerMsg(socket,split[1],p.addr,split[2])

		elif split[0] == 'die':
			for p in players:
				sendPlayerDie(socket,p.addr,split[1])

		




async def main():
    server = socketserver.UDPServer((HOST,8008), MyUDPHandler)
    print(f'Serving on '+str(HOSTname)+" "+str(8008))
    server.serve_forever()

asyncio.run(main())
