import pygame
import ui
special = [ui.textbutton("IP: ",370, 185, 300, 75),ui.textbutton("Port: ", 370, 285, 300, 75)]
complete = ['None','None']
def drawStart(screen, titlefont, state,events,title):
	global special
	global complete

	if title == "Platformer":
		pygame.draw.rect(screen, (153,0,0), (0,0,250,85))
		pygame.draw.rect(screen, (41,41,41), (0,0,220,70))
	else:
		pygame.draw.rect(screen, (153,0,0), (0,0,350,85))
		pygame.draw.rect(screen, (41,41,41), (0,0,320,70))

	char1 = titlefont.render(title, 1, (255,255,255))
	screen.blit(char1, (10, 10))
	startbutton3 = ui.button("Done", 370, 385, 300, 75)
	startbutton3.render(screen)

	ip = special[0].render(screen,events)
	port = special[1].render(screen,events)

	if ip is not None:
		complete[0] = ip
	if port is not None:
		complete[1] = port

	if startbutton3.pressed(events):
		return(complete)


	


