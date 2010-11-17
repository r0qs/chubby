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
        self.dx = 5             #distance per frame (velocity) covered in x
        self.dy = 0             #distance per frame (velocity) covered in y
        self.ddx = 0		#acceleration on the x speed
        self.ddy = 0		#acceleration on the y speed
        self.real_x = 0     # real x position (related to the start of the level)
        self.real_y = self.y     # real y position (related to the start of the level)
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

        
        # animation
        self.animate[self.animation_key](t)

    def stop(self):
        self.dx = 0
        
    # Receives the 'ground' or 'killer' list (of 4-uples) from Game.py and returns:
    # 0: if there's no collision at all
    # 1: if the sprite collides with the object from the top
    # 2: if the sprite collides with the object from the left
    def collides_with_objects(self, objects_list):
        for obj in objects_list:
            if self.y + self._h >= obj[1]:
                return 1
        
            
   

    #FIXME:
    # The jump sucks... but i will fix this - Diego
    def doJump(self):

        if self.onGround:
            print "jump"
            self.animation_key = "jumping"
            self.ddy = -0.15
            self.onGround = False
            self.onJump = True
            self.dy += 4
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
