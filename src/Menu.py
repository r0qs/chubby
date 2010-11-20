import pygame
from pygame.locals import *

class Option:

	# selected_size = the size of the surface when she's selected
	# resize_frame = how larger/small one surface can be in one iteration (0.13 = 13%)
	# function = the function assigned to a option. The function need to be implemented ...(obvious xD)
	def __init__(self,x,y,width,height,image_path,selected_size=2,resize_frame=0.07,function=None):
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
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		self.function = function
		self.selected = False
		
	#FIXME: pygame.transform.scale is not working like i wanted. The image's resolution became so poor after a while.
	def mouse_on(self,screen):
		if self.width < self.max_width:
			self.image = pygame.transform.scale(self.image,(self.width*(1+self.resize_frame),self.height*(1+self.resize_frame)))
			self.width , self.height = self.image.get_size()
			self.rect = self.image.get_rect(center=(self.center)) 
			self.selected = True
			
	def mouse_off(self,screen):
		if self.width > self._width:
			self.image = pygame.transform.scale(self.image,(self.width*(1-self.resize_frame),self.height*(1-self.resize_frame)))
			self.width , self.height = self.image.get_size()
			self.rect = self.image.get_rect(center=(self.center))
			self.selected = False
	
	def get_rect(self):
		return self.rect
		
	def activate(self):
		if self.selected:
			self.function()
		
	def show(self,screen):
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
		
	def show (self,screen):
		screen.blit(self.image,self.rect)
		
	def collides_with_objects(self,object_list):
		return self.rect.colliderect(object_list)
		
	def select(self,option):
		option.is_Selected = True

class Menu:
	def __init__(self,width,height,options_list):
		
	


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
	option1 = Option(200,200,32,32,'images/1.png')
	option2 = Option(200,500,32,32,'images/2.png')
	
	menu_screen.blit(background, (0, 0))
	cursor.show(menu_screen)
	option2.show(menu_screen)
	pygame.display.flip()
	
	# Event loop
	while 1:
#		pygame.event.pump()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.display.quit
				return
			elif event.type == MOUSEMOTION:
				pygame.mouse.get_pos()
				cursor.update()
				if cursor.collides_with_objects(option1.get_rect()):
					option1.mouse_on(menu_screen)
				else:
					option1.mouse_off(menu_screen)

		menu_screen.blit(background, (0, 0))
		option1.show(menu_screen)
		cursor.show(menu_screen)
		pygame.display.flip()
	
if __name__ == '__main__': main()
