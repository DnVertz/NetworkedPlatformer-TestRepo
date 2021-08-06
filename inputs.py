import pygame 
import ui 

def run(state,player,events,msgbox,sock,server,clientid,deathtimeout):
	shooting = False

	for event in events:
		if event.type == pygame.KEYDOWN:
			keys2 = pygame.key.get_pressed()
			if keys2[pygame.K_RETURN]:
				return True

	if msgbox == False:
		keys = pygame.key.get_pressed()
		mouse_buttons = pygame.mouse.get_pressed()
		if keys[pygame.K_d]:
			player.moveRight()
					
			
		if keys[pygame.K_a]:
				player.moveLeft()

		if keys[pygame.K_SPACE]:
				player.moveUp()

		if keys[pygame.K_1]:
				player.weapon_one()

		if keys[pygame.K_2]:
				player.weapon_two()

		if keys[pygame.K_3]:
				player.weapon_three()

		if mouse_buttons[0]:
			shooting = True
			player.shoot(sock,server,clientid,deathtimeout)


		if keys[pygame.K_r]:
			if shooting == False:
				player.reload()

		

	

	




def handleMouse(pygame, player):
	player_pos = pygame.math.Vector2(player.x, player.y)
	mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
	aim = mouse_pos - player_pos
	angle = aim.angle_to(pygame.math.Vector2(1, 0))
	#player.setAngle(angle)



