from Game import *
from Menu import *

def new_game_function():
	game_main()
	

def option_function():
	main()
	


def main():

	width = 1024
	height = 768
	pygame.display.init
	menu_screen = pygame.display.set_mode((width,height))
	
	# Background
	background = pygame.image.load(os.path.join('', 'images', 'menu_bg.jpg'))
	background = background.convert()
	
	# Cursor
	pygame.mouse.set_visible(False)
	cursor = Cursor(16,16,'images/cursor.png')
	
	#Options in menu
	new_game = Option(200,200,173,89,'images/little.png','images/big.png',new_game_function, 1.42)

	# Menu
	menu = Menu()
	menu.append(new_game)
	
	menu_screen.blit(background, (0, 0))
	cursor.draw(menu_screen)
	menu.draw(menu_screen)
	pygame.display.flip()
	
	# Event loop
	while 1:
		menu.update(cursor)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.display.quit
				sys.exit()
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
				return
			elif event.type == MOUSEMOTION:
				pygame.mouse.get_pos()
				cursor.update()
			elif event.type == MOUSEBUTTONDOWN:
				menu.activate()

		menu_screen.blit(background, (0, 0))
		menu.draw(menu_screen)
		cursor.draw(menu_screen)
		pygame.display.flip()
	
if __name__ == '__main__': main()
