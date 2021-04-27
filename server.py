import threading, uuid, asyncio
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
players_lock = threading.Lock()


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
	data = "init;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+"\n"
	player.socket.sendto(data.encode('UTF-8'),player.addr)


def sendPlayerSpawn(player,addr):
	data = "spawn;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+"\n"
	player.socket.sendto(data.encode('UTF-8'),addr)

def sendPlayerJoin(player):
	data = "join;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+"\n"
	broadcast(data.encode('UTF-8'))

def sendPlayerLeave(player,addr):
	data = "leave;"+str(player.id)+"\n"
	player.socket.sendto(data.encode('UTF-8'),addr)

def sendPlayerPos(player,addr):
	data = "pos;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+"\n"
	player.socket.sendto(data.encode('UTF-8'),addr)



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
	def __init__(self, socket,addr):
		self.id = uuid.uuid1()
		self.socket = socket
		self.addr = addr
		self.x = 0
		self.y = 0
		self.vx = 0
		self.vy = 0
	def setPosition(self, x, y):
		self.x = x
		self.y = y
	def getPosition(self):
		return (self.x, self.y)



class MyUDPHandler(socketserver.DatagramRequestHandler):
	def handle(self):
		data = self.request[0].strip()
		socket = self.request[1]
		#socket.settimeout(1.0)
		data = data.decode()
		split = data.split(";")

		if split[0] == 'join':
			player = Player(socket,self.client_address)
			playerID = player.id
			players.append(player)
			sendPlayerInit(player, self.client_address,socket) #send init id and pos to player
			for p in players:
				print(p.id)
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
					for p in players:
						if str(p.id) != str(players[i].id):
							sendPlayerPos(players[i],p.addr)
							
		elif split[0] == 'leave':
			for i in range(len(players)):
				if str(players[i].id) == split[1]:
					for p in players:
						if str(p.id) != str(players[i].id):
							sendPlayerLeave(players[i],p.addr)
						players.remove(players[i])
						
					break
							

async def main():
    server = socketserver.UDPServer((HOST,8008), MyUDPHandler)
    print(f'Serving on '+str(HOSTname)+" "+str(8008))
    server.serve_forever()

asyncio.run(main())
