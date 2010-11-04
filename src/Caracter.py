import pygame
from pygame.locals import *

class Caracter(pygame.sprite.Sprite):
    x,y = (32,130)
    def __init__(self, name, img, frames=1, width=32, height=32, fps=5):
        self.name = name
        self.alive = True
        pygame.sprite.Sprite.__init__(self)
        original_width, original_height = img.get_size()
        self._w = width
        self._h = height
        self._framelist = []
        for i in xrange(int(original_width/width)):
            self._framelist.append(img.subsurface((i*width,0,width,height)))
        self.image = self._framelist[0]
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0
        self.update(pygame.time.get_ticks(), 100, 100)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return (self.x,self.y)

    def update(self, t, width, height):
        # postion
        self.x+=1
        if(self.x > width):
            self.x = -self._w

        # animation
        if t - self._last_update > self._delay:
            self._frame += 1
            if self._frame >= len(self._framelist):
                self._frame = 0
            self.image = self._framelist[self._frame]
            self._last_update = t

