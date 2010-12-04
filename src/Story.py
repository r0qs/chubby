import pygame
from pygame.locals import *
from Sound import *
import sys, os

class Story:

	def __init__(self,folder, n_frames):
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((1024, 768))
		self.story = []
		for i in range(0,n_frames):
			self.story.append(pygame.image.load(os.path.join('', 'stories/' + folder, str(i+1) + '.jpg')))
		self.actual_image = self.story[0]

	def _next_image(self):
		fill_surf = pygame.Surface((1024,768))
		fill_surf.fill((10,10,10))
		alpha = 0
		fill_surf.set_alpha(alpha)
		while alpha < 255:
			self.clock.tick(25)
			alpha+=35
			fill_surf.set_alpha(alpha)
			self.screen.blit(fill_surf, (0,0))
			pygame.display.flip()
		self.story.pop(0)
		self.actual_image = self.story[0]
		while alpha > 0:
			self.clock.tick(25)
			alpha-=35
			fill_surf.set_alpha(alpha)
			self.screen.blit(self.actual_image, (0,0))
			self.screen.blit(fill_surf, (0,0))
			pygame.display.flip()
			
	def play(self):
		adj_x, adj_y = 0 , 0
		running = True
		while running:
			self.clock.tick(25)
			self.screen.blit(self.actual_image, (0 - adj_x, 0 - adj_y))
			adj_x += 0.5
			adj_y += 0.5
			if self.actual_image.get_width() < self.screen.get_width() + adj_x or self.actual_image.get_height() < self.screen.get_height() + adj_y:
				adj_x = 0
				adj_y = 0
				if len(self.story) == 1:
					running = False
				else: self._next_image()
			for e in pygame.event.get():
				if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
					running = False
			pygame.display.flip()
        
    
