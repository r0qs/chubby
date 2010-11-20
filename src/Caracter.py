import pygame
from pygame.locals import *

#TODO:
# collision detection


class Caracter(pygame.sprite.Sprite):
    x,y = (0,0)
    def __init__(self, name, img, frames=1, width=115, height=115, fps=25):
        self.animate = {
	        'running':self._anim_run,
	        'jumping':self._anim_jump
	}
	    
        self.animation_key = "running"
        
        self.name = name
        self.onGround = True
        self.onJump = False    
        self.forceJump = 2
        
        self.state = 0
        pygame.sprite.Sprite.__init__(self)
        self._w = width
        self._h = height        #size of caracter frames WxH
        self._y = self.y        #ground level
        self.dx = 4             #distance per frame (velocity) covered in x
        self.dy = 0             #distance per frame (velocity) covered in y
        self.ddx = 0		#acceleration on the x speed
        self.ddy = 0		#acceleration on the y speed
        self.real_x = 200     # real x position (related to the start of the level)
        self.real_y = self.y     # real y position (related to the start of the level)
        self.screen = pygame.display.get_surface().get_rect()
        self._framelist = getFrameList(img, self._w, self._h)
        self.image = self._framelist[0]
        self.rect = self.image.get_rect()
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0
        self.update(pygame.time.get_ticks(), 115, 115, (4, 0))

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return (self.x,self.y)

    def update(self, t, width, height, cam_speed):
        #velocity
        self.dx += self.ddx
        self.dy += self.ddy
        
        # postion
        self.x += self.dx - cam_speed[0]
        self.y -= self.dy - cam_speed[1]
        
        #real position (according to the init of the level)
        self.real_x += self.dx
        #print self.real_x
        
        #emulate gravity
        self.ddy = -0.15
        # animation
        self.animate[self.animation_key](t)

    def stop(self):
        self.dx = 0
    
    
    #FIXME: Essa colisao nao esta boa, pq ela esta checando colisao de rect do sprite com os rects dos objetos. 
    #Seria legal se fosse colisao de pixel do sprite com os rects dos objetos
        
    # Receives the 'ground' or 'killer' list (of 4-uples) from Game.py and returns:
    # -1, -1: if there's no collision at all
    # obj, 1: if the sprite collides with the object from the top
    # obj, 2: if the sprite collides with the object from the left
    def collides_with_objects(self, objects_list):
        ac = 0
        while ac < len(objects_list):

            if (self.real_x + self._w) >= objects_list[ac][0] and self.real_x <= objects_list[ac][0] + objects_list[ac][2] \
            and self.y + self._h >= objects_list[ac][1]:
            
                try:
                    if (self.y + self._h) > objects_list[ac + 1][1] + 1 and self.y < objects_list[ac + 1][1] + objects_list[ac + 1][3] \
                    and self.real_x + self._w > objects_list[ac + 1][0] and self.real_x < objects_list[ac + 1][0] + objects_list[ac + 1][2]:
                    
                        return objects_list[ac + 1], 2
                        
                except IndexError:
                    return objects_list[ac], 1
                return objects_list[ac], 1
                
            if (self.y + self._h) > objects_list[ac][1] + 1 and self.y < objects_list[ac][1] + objects_list[ac][3] \
            and self.real_x + self._w > objects_list[ac][0] and self.real_x < objects_list[ac][0] + objects_list[ac][2]:
            
                return objects_list[ac], 2
            ac += 1
        
        return -1, -1

    def put_on_ground_running(self, ground_y):
        self.dy = 0
        self.ddy = 0
        self.animation_key = "running"
        self.y = ground_y - self._h
        self.forceJump = 2
        self.onGround = True
        self.onJump = False

    #FIXME:
    # The jump sucks... but i will fix this - Diego
    def doJump(self):

        if self.onGround:
            self.animation_key = "jumping"
            self.onGround = False
            self.onJump = True
            self.ddy += 4
        elif self.onJump:
            if(self.dy > 0):
                self.forceJump -= 0.3
                self.ddy += self.forceJump
            if self.forceJump <= 0:
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
