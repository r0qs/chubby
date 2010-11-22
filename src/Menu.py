import pygame
from pygame.locals import *

from Game import *


class Option:

	# selected_size = the size of the surface when she's selected (2 = double size)
	# resize_frame = how larger/small one surface can be in one iteration (0.13 = 13%)
	# function = the function assigned to a option. The function need to be implemented ...(obvious xD)
	def __init__(self,x,y,width,height,image_path,big_image_path,function,selected_size=2,resize_frame=0.10):
		self.x = x
		self.y = y
		self.center = x+width/2,y+height/2
		self._width = width
		self._height = height
		self.width = width
		self.max_width = width*selected_size
		self.resize_frame = resize_frame
		self.height = height
		self.image = pygame.image.load(image_path)
		self.little_image = self.image.copy()
		self.big_image = pygame.image.load(big_image_path)
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		self.function = function
		self.selected = False
		self.change_image = False
		
	def mouse_on(self):
		self.selected = True
		if self.width < self.max_width:
			self.image = pygame.transform.scale(self.image,(self.width*(1+self.resize_frame),self.height*(1+self.resize_frame)))
			self.change_image = False
		else:
			if not self.change_image:
				self.change_image = True
				self.image = self.big_image.copy()
		self.width , self.height = self.image.get_size()
		self.rect = self.image.get_rect(center=(self.center)) 
			
		
			
	def mouse_off(self):
		self.selected = False
		if self.width > self._width:
			self.image = pygame.transform.scale(self.image,(self.width*(1-self.resize_frame),self.height*(1-self.resize_frame)))
			self.change_image = False
		else:
			if not self.change_image:
				self.change_image = True
				self.image = self.little_image.copy()
		self.width , self.height = self.image.get_size()
		self.rect = self.image.get_rect(center=(self.center))
		
	
	def get_rect(self):
		return self.rect
		
	def activate(self):
		if self.selected:
			self.function()
		
	def draw(self,screen):
		screen.blit(self.image,self.rect)

class Cursor:
	def __init__(self,width,height,image_path):
		self.width = width
		self.height = height
		self.x , self.y = pygame.mouse.get_pos()
		self.image = pygame.image.load(image_path)
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		
	def update(self):
		self.x , self.y = pygame.mouse.get_pos()
		self.rect.left = self.x
		self.rect.top = self.y
		
	def draw (self,screen):
		screen.blit(self.image,self.rect)
		
	def on_option(self,option):
		menu_rect = option.get_rect()
		return self.rect.colliderect(option)
		
	def select(self,option):
		option.is_Selected = True

class Menu:
	def __init__(self):
		self.options = []
	
	def append(self,option):
		self.options.append(option)
			
	def update(self,cursor):
		for option in self.options:
			if cursor.on_option(option):
				option.mouse_on()
			else:
				option.mouse_off()
				
	def draw(self,screen):
		for option in self.options:
			option.draw(screen)
			
	def activate(self):
		for option in self.options:
			option.activate()

def new_game_function():
	game_main()
##	new_game_menu = pygame.display.set_mode((1024,640))
##	background = pygame.Surface(new_game_menu.get_size())
##	background = background.convert()
##	background.fill((100, 250, 250))
##	pygame.mouse.set_visible(False)
##	cursor = Cursor(16,16,'images/cursor.png')
##	voltar = Option(300,100,62,62,'images/little.png','images/big.png',option_function)
##	menu_n = Menu()
##	menu_n.append(voltar)
##	new_game_menu.blit(background, (0, 0))
##	cursor.draw(new_game_menu)
##	menu_n.draw(new_game_menu)
##	pygame.display.flip()
##	
##		# Event loop
##	while 1:
###		pygame.event.pump()
##		menu_n.update(cursor)
##		for event in pygame.event.get():
##			if event.type == QUIT:
##				pygame.display.quit
##				return
##			elif event.type == MOUSEMOTION:
##				pygame.mouse.get_pos()
##				cursor.update()
##			elif event.type == MOUSEBUTTONDOWN:
##				menu_n.activate()


##		new_game_menu.blit(background, (0, 0))
##		menu_n.draw(new_game_menu)
##		cursor.draw(new_game_menu)
##		pygame.display.flip()
	

def option_function():
	main()
	


def main():

	width = 1024
	height = 640
	pygame.display.init
	menu_screen = pygame.display.set_mode((width,height))
	
	# Background
	background = pygame.Surface(menu_screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))
	
	# Cursor
	pygame.mouse.set_visible(False)
	cursor = Cursor(16,16,'images/cursor.png')
	
	#Options in menu
	new_game = Option(200,200,62,62,'images/little.png','images/big.png',new_game_function)
	
	# Menu
	menu = Menu()
	menu.append(new_game)
	
	menu_screen.blit(background, (0, 0))
	cursor.draw(menu_screen)
	menu.draw(menu_screen)
	pygame.display.flip()
	
	# Event loop
	while 1:
#		pygame.event.pump()
		menu.update(cursor)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.display.quit
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
