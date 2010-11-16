import pygame
from pygame.locals import *

#TODO:
# collision detection


class Caracter(pygame.sprite.Sprite):
    x,y = (0,0)
    a = 2
    # Those variables will need to become global - Diego
    def __init__(self, name, img, frames=1, width=115, height=115, fps=25):
        self.animate = {
	        'running':self._anim_run,
	        'jumping':self._anim_jump
	}
	    
        self.animation_key = "running"
        
        self.name = name
        self.onGround = True
        self.onJump = False    
        self.forceJump = 0
        
        self.state = 0
        pygame.sprite.Sprite.__init__(self)
        self._w = width
        self._h = height        #size of caracter frames WxH
        self._y = self.y        #ground level
        self.jumpMaxHeight = 20 #maximum height of the jump
        self.dx = 5             #distance per frame (velocity) covered in x
        self.dy = 0             #distance per frame (velocity) covered in y
        self.ddx = 0		#acceleration on the x speed
        self.ddy = 0		#acceleration on the y speed
        self.screen = pygame.display.get_surface().get_rect()
        self._framelist = getFrameList(img, self._w, self._h)
        self.image = self._framelist[0]
        self.rect = self.image.get_rect()
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0
        self.update(pygame.time.get_ticks(), 115, 115)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return (self.x,self.y)

    def update(self, t, width, height):
        #velocity
        self.dx += self.ddx
        self.dy += self.ddy
        
        # postion
        self.x += self.dx
        self.y -= self.dy
            
        # fast solution for the ground colision (FIXME) ground = 325
        if self.y > 205:
            self.dy = 0
            self.ddy = 0
            self.animation_key = "running"
            self.y = 205
            self.a = 2
            self.onGround = True
            self.onJump = False
        
        # animation
        self.animate[self.animation_key](t)

    def stop(self):
        self.dx = 0
   

#FIXME:
# The jump sucks... but i will fix this - Diego
    def doJump(self):

        if self.onGround:
            print "jump"
            self.animation_key = "jumping"
            self.ddy = -0.15
            self.onGround = False
            self.onJump = True
            self.forceJump = 4
            self.dy += self.forceJump
        elif self.onJump:
            if(self.dy > 0):
                self.a -= 0.3
                print self.a
                self.dy += self.a
            if self.a <= 0:
                self.onJump = False
                
            
#    def doRoll():
#    def doSprint():
#    def doGetDown():
#    def doClimb():

    def _anim_run(self, t):
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
    def _anim_jump(self, t):
	    self.image = self._framelist[7]
	    self._frame = 7
	    self._last_update = t
    
    #def _anim_roll():
    #def _anim_get_down():
    #def _anim_climb():
	


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
