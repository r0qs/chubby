import pygame
from pygame.locals import *

#TODO:
# collision detection


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(rect)
        self.surface = pygame.Surface((rect[2],rect[3]))
        self.mask = self.mask = pygame.mask.from_surface(self.surface)
        self.mask.fill()
