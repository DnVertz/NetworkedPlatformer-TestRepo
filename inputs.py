import pygame 
import ui 

def run(state,player):
	keys = pygame.key.get_pressed()
	

	if keys[pygame.K_d]:
			player.moveRight()
			
	
	if keys[pygame.K_a]:
			player.moveLeft()

	if keys[pygame.K_SPACE]:
			player.moveUp()
	if keys:
		return True


def handleMouse(pygame, player):
	player_pos = pygame.math.Vector2(player.x, player.y)
	mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
	aim = mouse_pos - player_pos
	angle = aim.angle_to(pygame.math.Vector2(1, 0))
	#player.setAngle(angle)



