import pygame
from pygame.locals import *

from Sound import *

import sys, os
from random import choice
import string


class Story:

	def __init__(self,folder, n_frames, frame_init, musicname):
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((1024, 768))
		self.story = []
		self.frames = n_frames
		#print frame_init, n_frames
		for i in range(0 ,n_frames):
			self.story.append(pygame.image.load(os.path.join('', 'stories/' + folder, str(i+1) + '.jpg')))
		#self.story = self.story[frame_init:n_frames]
		
		self.actual_image = self.story[0]
		self.bg_music = Music()
		self.bg_music.load_music(musicname)

		pygame.font.init()
		self.buttons = generate_buttons_sequence(2)
		self.size = len(self.buttons)
		self.font = pygame.font.Font(os.path.join('', 'data', 'actionj.ttf'), 80)
		self.font.set_bold(True)

	def test_commands(self, frame):
		if frame > self.frames:
			return False, -2
		running = True
		hit = False
		count = 0
		iterator = 0
		showb = False
		adj_x, adj_y = 0 , 0
		button = None
		button_rect = pygame.Rect(512,520,200,200)
		self.actual_image = self.story[frame-1]
		while running:
			self.clock.tick(25)
			self.screen.blit(self.actual_image, (0 - adj_x, 0 - adj_y))
			adj_x += 0.5
			adj_y += 0.5
			if self.actual_image.get_width() < self.screen.get_width() + adj_x or self.actual_image.get_height() < self.screen.get_height() + adj_y:
				print count, count == len(self.buttons)
				if count == self.size:
					return True, frame+1
				elif len(self.buttons) <= 0:
					return False, -1
			if (iterator % 30) == 0:
				showb = True
			if len(self.buttons) > 0 and (iterator % 30) == 0 and showb:
				b = self.buttons.pop(0)
			if b == 'key_up':
				butt = 'up'
				button = pygame.image.load(os.path.join('', 'images/' + b + '_UP' + '.png'))
				if (iterator % 4) == 0:
					button = pygame.image.load(os.path.join('', 'images/' + b + '_DOWN' + '.png'))
			elif b == 'key_down':
				butt = 'down'
				button = pygame.image.load(os.path.join('', 'images/' + b + '_UP' + '.png'))
				if (iterator % 4) == 0:
					button = pygame.image.load(os.path.join('', 'images/' + b + '_DOWN' + '.png'))
			elif b == 'key_right':
				butt = 'right'
				button = pygame.image.load(os.path.join('', 'images/' + b + '_UP' + '.png'))
				if (iterator % 4) == 0:
					button = pygame.image.load(os.path.join('', 'images/' + b + '_DOWN' + '.png'))
			elif b == 'key_left':
				butt = 'left'
				button = pygame.image.load(os.path.join('', 'images/' + b + '_UP' + '.png'))
				if (iterator % 4) == 0:
					button = pygame.image.load(os.path.join('', 'images/' + b + '_DOWN' + '.png'))
			#if button != None:
			#	self.screen.blit(button, button_rect)
			for e in pygame.event.get():
				if e.type == QUIT:
					sys.exit()
				if e.type == KEYDOWN and e.key == K_ESCAPE:
					running = False
				if e.type is KEYDOWN:
					key = pygame.key.name(e.key)
					print key, butt, key == butt
					if key == butt:
						count = count + 1
						button = None
						hit = True
					else:
						hit = False
						button = None
						return False, -1
			iterator = iterator + 1
			pygame.display.flip()

	def play(self, frame):
		running = True
		adj_x, adj_y = 0 , 0
		self.actual_image = self.story[frame-1]
		while running:
			self.clock.tick(25)
			self.screen.blit(self.actual_image, (0 - adj_x, 0 - adj_y))
			adj_x += 0.5
			adj_y += 0.5
			if self.actual_image.get_width() < self.screen.get_width() + adj_x or self.actual_image.get_height() < self.screen.get_height() + adj_y:
				return True, frame+1
			for e in pygame.event.get():
				if e.type == QUIT:
					sys.exit()
				if e.type == KEYDOWN and e.key == K_ESCAPE:
					running = False
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
		print self.story
		print self.story.pop(0)
		self.actual_image = self.story[0]
		while alpha > 0:
			self.clock.tick(25)
			alpha-=35
			fill_surf.set_alpha(alpha)
			self.screen.blit(self.actual_image, (0,0))
			self.screen.blit(fill_surf, (0,0))
			pygame.display.flip()

	def play_loop(self, frame):
		adj_x, adj_y = 0 , 0
		running = True
		posframe = frame - 1
		self.actual_image = self.story[posframe]
		if not self.bg_music.get_busy_music():
			self.bg_music.play_load_music(1)
		while running:
			self.clock.tick(25)
			self.screen.blit(self.actual_image, (0 - adj_x, 0 - adj_y))
			adj_x += 0.5
			adj_y += 0.5
			if self.actual_image.get_width() < self.screen.get_width() + adj_x or self.actual_image.get_height() < self.screen.get_height() + adj_y:
				adj_x = 0
				adj_y = 0
				#if len(self.story) == 1:
				print len(self.story)
				if len(self.story) == 1:
					running = False
				else: self._next_image()
			for e in pygame.event.get():
				if e.type == QUIT:
					sys.exit()
				if e.type == KEYDOWN and e.key == K_ESCAPE:
					running = False
			pygame.display.flip()
		self.bg_music.fadeout_music(1)


def generate_buttons_sequence(length):
	buttons = []
	chars = ['key_up', 'key_down', 'key_right', 'key_left']
	for i in range(0,length):
		c = choice(chars)
		while c in buttons: c = choice(chars)
		buttons.append(c)
	return buttons
