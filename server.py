import threading, uuid, asyncio
import socket
import socketserver


PORT = 8008
#Jank cannot describe this solution
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#s.connect(("8.8.8.8", 8008))
#HOST = str(s.getsockname()[0])
#s.close()
HOST = ''


players = []
players_lock = threading.Lock()

"""
	Packets

	Inbound (to server)

	Player Pos: sent on player position change, scope: player
		pos;<X>;<Y>
	
	Outbound (to clients)

	Player Init: sent on join, scope: player
		init;<ID>;<X>;<Y>
	Player Join: sent on join, scope: all
		join;<ID>;<X>;<Y>
	Player Pos: sent on player positon change, scope: all
		pos;<ID>;<X>;<Y>

"""

def broadcast(data):
	for player in players:

		try:
			player.conn.write(data)
			#player.conn.drain()
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

def sendPlayerLeave(playerID):
	data = "leave;"+str(playerID)+"\n"
	broadcast(data.encode('UTF-8'))

def sendPlayerPos(player,addr):
	data = "pos;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+"\n"
	player.socket.sendto(data.encode('UTF-8'),addr)


class PositionUpdate:
	def __init__(self, pid, x: int, y: int):
		self.id = pid
		self.x = x
		self.y = y
	def updatePlayer(self):
		#players_lock.acquire()
		for i in range(len(players)):
			if players[i].id == self.id:
				players[i].x = self.x
				players[i].y = self.y
				break
		#players_lock.release()
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
		#print(self.request)
		data = self.request[0].strip()
		socket = self.request[1]
		socket.settimeout(1.0)
		data = data.decode()
		split = data.split(";")
		if split[0] == 'join':
			#print("ya")
			player = Player(socket,self.client_address)
			playerID = player.id
			#print (playerID)

			players.append(player)
			sendPlayerInit(player, self.client_address,socket) #send init id and pos to player
			for p in players:
				print(p.id)
				if p is not player:
					sendPlayerSpawn(p,player.addr)
					sendPlayerSpawn(player,p.addr)

				else:		
					sendPlayerSpawn(player,p.addr)
				#sendPlayerJoin(player) #broadcast init id and pos to all players
		
		elif split[0] == 'pos':

			for i in range(len(players)):
				print(players[i].id)
				if str(players[i].id) == split[1]:

					players[i].x = split[2]
					players[i].y = split[3]

					for p in players:
						if str(p.id) != str(players[i].id):
							print(p.id)
							print(players[i].id)
							sendPlayerPos(players[i],p.addr)

		

		

				

				


async def main():
    server = socketserver.UDPServer((HOST,8008), MyUDPHandler)
    #server._handle_request_noblock()
    #dserver.max_packet_size = 8192*2
    #server.setblocking(False)


    #
    #addr = server.sockets[0].getsockname()
    print(f'Serving on '+str(HOST)+" "+str(8008))
    server.serve_forever()

asyncio.run(main())
