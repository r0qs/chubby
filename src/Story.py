import pygame
from pygame.locals import *

from Sound import *

import sys, os
from random import choice
import string


class Story:

	def __init__(self,folder, n_frames):
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((1024, 768))
		self.story = []
		for i in range(0,n_frames):
			self.story.append(pygame.image.load(os.path.join('', 'stories/' + folder, str(i+1) + '.jpg')))
		self.actual_image = self.story[0]

		pygame.font.init()
		#self.buttons = generate_buttons_sequence(5)
		self.buttons = ['q','w','e','r','t']
		self.font = pygame.font.Font(os.path.join('', 'data', 'buttons.ttf'), 70)
		self.font.set_bold(True)

	def _next_image_wiyh_crazy_buttons(self):
		return

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

	def play(self, draw_buttons=False):
		adj_x, adj_y = 0 , 0
		running = True
		hit = False
		count = 0
		while running:
			self.clock.tick(26)
			self.screen.blit(self.actual_image, (0 - adj_x, 0 - adj_y))
			adj_x += 0.5
			adj_y += 0.5
			if len(self.buttons) > 0 and draw_buttons:
				char = self.buttons.pop(0)
				button = self.font.render(char, 1, (0,200,0))
				self.screen.blit(button, (600,500)) # blit actual_button
			if self.actual_image.get_width() < self.screen.get_width() + adj_x or self.actual_image.get_height() < self.screen.get_height() + adj_y:
				adj_x = 0
				adj_y = 0
				if len(self.story) == 1:
					running = False
				elif hit and draw_buttons:
					self._next_image_wiyh_crazy_buttons()
				else: self._next_image()
			for e in pygame.event.get():
				if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
					running = False
				if e.type is KEYDOWN:
					key = pygame.key.name(e.key)
					if draw_buttons:
						if key == char:
							count = count + 1
							print key
						else:
							hit = False
			pygame.display.flip()

def generate_buttons_sequence(length):
	buttons = []
	chars = string.letters + string.digits
	for i in range(0,length):
		buttons.append(choice(chars))
	return buttons
