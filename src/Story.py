import pygame
from pygame.locals import *

from Sound import *

import sys, os
from random import choice
import string


class Story:

	def __init__(self,folder, n_frames, musicname):
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((1024, 768))
		self.story = []
		for i in range(0,n_frames):
			self.story.append(pygame.image.load(os.path.join('', 'stories/' + folder, str(i+1) + '.jpg')))
		self.actual_image = self.story[0]
		self.bg_music = Music()
		self.bg_music.load_music(musicname)

		pygame.font.init()
		#self.buttons = generate_buttons_sequence(5)
		self.buttons = ['q','w','e','r','t']
		self.font = pygame.font.Font(os.path.join('', 'data', 'buttons.ttf'), 70)
		self.font.set_bold(True)

	def test_commands(self):
		background = pygame.Surface(self.screen.get_size())
		background = background.convert()
		running = True
		hit = False
		count = 0
		iterator = 0
		adj_x, adj_y = 0 , 0
		while running:
			self.clock.tick(25)
			self.screen.blit(self.actual_image, (0 - adj_x, 0 - adj_y))
			adj_x += 0.5
			adj_y += 0.5
			if self.actual_image.get_width() < self.screen.get_width() + adj_x or self.actual_image.get_height() < self.screen.get_height() + adj_y:
				adj_x = 0
				adj_y = 0

			if len(self.buttons) > 0 and not (iterator % 35):
				char = self.buttons.pop(0)
				button = self.font.render(char, 1, (100,255,100))
				button_rect = pygame.Rect(600,500,200,200)
				if button != None:
					background.blit(button, button_rect)
					self.screen.blit(background, (0, 0))# ta horrivel!!
			for e in pygame.event.get():
				if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
					running = False
				if e.type is KEYDOWN:
					key = pygame.key.name(e.key)
					if key == char:
						count = count + 1
						hit = True
					else:
						hit = False
						button = None
						return False
			print "hit: " + str(hit) + "count: " + str(count)
			if count == 5:
				return True
			elif iterator > 400:  #arranjar outra forma de sair:|
				return False
			iterator = iterator + 1
			pygame.display.flip()

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
		self.bg_music.play_load_music(1)
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
		self.bg_music.fadeout_music(1)


def generate_buttons_sequence(length):
	buttons = []
	chars = string.letters + string.digits
	for i in range(0,length):
		buttons.append(choice(chars))
	return buttons
