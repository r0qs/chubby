import pygame
from pygame.locals import *

#TODO:
# collision detection


class Caracter(pygame.sprite.Sprite):
    x,y = (0,0)
    # Those variables will need to become global - Diego
    gravity = 1
    maxGravity = -10
    def __init__(self, name, img, frames=1, width=115, height=115, fps=25):
        self.name = name
        self.onGround = True
        self.onJump = False    
        self.impulse = 0
        self.forceJump = 0
        
        self.state = 0
        pygame.sprite.Sprite.__init__(self)
        self._w = width
        self._h = height        #size of caracter frames WxH
        self._y = self.y        #ground level
        self.jumpMaxHeight = 20 #maximum height of the jump
        self.dx = 5             #distance per frame covered in x
        self.dy = 0             #distance per frame covered in y
        self.screen = pygame.display.get_surface().get_rect()
        self._framelist = getFrameList(img, self._w, self._h)
        self.image = self._framelist[0]
        self.rect = self.image.get_rect()
        self._start = pygame.time.get_ticks()
        self._delay = 300 / fps
        self._last_update = 0
        self._frame = 0
        self.update(pygame.time.get_ticks(), 115, 115)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return (self.x,self.y)

    def update(self, t, width, height):
        # postion
        if self.state == 11:        #jump state
            self.doJump()
            self.state = 0
        # update x coordinates
        self.x += self.dx
        if(self.x > width):
            self.x = -self._w
        # update y coordinates
        # Jump 
        if self.onJump:
            if self.forceJump < self.maxGravity:
                self.forceJump = self.maxGravity
            else:    
                self.forceJump -= self.gravity
                
            self.dy += self.forceJump 
        elif not self.onGround:
            self.dy -= self.gravity
        
        self.y -= self.dy
            
        # fast solution for the ground colision (FIXME) ground = 325
        if self.y > 325:
            self.dy = 0
            self.y = 325
            self.onGround = True
            self.onJump = False
        
        # animation
        if t - self._last_update > self._delay:
            self._frame += 1
            if self._frame >= len(self._framelist):
                self._frame = 0
            if self.onGround:
                self.image = self._framelist[self._frame]
            elif self.dy < 0:
                self.image = self._framelist[5]
                self.dy = 1
                self.onGround = True
            self._last_update = t

    def stop(self):
        self.dx = 0

#FIXME:
# jump need some BLABLABURG to stop the incrementing/decrementing of dy, i thing the collision detection help to solve this problem
    def doJump(self):
        if self.onGround:
            print "jump"
            self.onGround = False
        if not self.onJump:
            self.impulse = 5
            self.forceJump = 5
            self.onJump = True
        else:
            if(self.impulse > 0 and self.forceJump > 2 ):
                self.forceJump += 10
                self.impulse -= 1
                
            
#    def doRoll():
#    def doSprint():
#    def doGetDown():
#    def doClimb():


def getFrameList(img, width, height):
        framelist = []
        img_width, img_height = img.get_size()
        for f in xrange(int(img_width/width)):
            framelist.append(img.subsurface(Rect(f*width,0,width,height)))
        return framelist

def getFrame(frameList):
    while True:
        for f in frameList:
            yield f
