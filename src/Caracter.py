import pygame
from pygame.locals import *

#TODO:
# collision detection


class Caracter(pygame.sprite.Sprite):
    x,y = (0,0)
    # Those variables will need to become global - Diego
    def __init__(self, name, img, frames=1, width=115, height=115, fps=25):
        
        self.animate = {
	        'running':self._anim_run,
	        'jumping':self._anim_jump,
	        'sprinting':self._anim_sprint,
	        'getting_down':self._anim_get_down
	}
	    
        self.animation_key = "running"
        
        self.sprint_timeout = 0
        self.name = name
        self.onGround = True
        self.sprinting = False
        self.pendingRoll = False
        self.falling = False
        self.tooHigh = False   
        self.forceJump = 2
        self.falling_time = 0
        
        self.state = 0
        pygame.sprite.Sprite.__init__(self)
        self._w = width
        self._h = height        #size of caracter frames WxH
        self._y = self.y        #ground level
        self.dx = 6             #distance per frame (velocity) covered in x
        self.dy = 0             #distance per frame (velocity) covered in y
        self.ddx = 0		#acceleration on the x speed
        self.ddy = 0		#acceleration on the y speed
        self.real_x = 0     # real x position (related to the start of the level)
        self.real_y = 0     # real y position (related to the start of the level)
        self._framelist = getFrameList(img, self._w, self._h)
        self.image = self._framelist[0]
        self.rect = Rect(self.image.get_rect())
        self.mask = pygame.mask.from_surface(self.image)
        
        
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0

    def set_pos(self, x, y):
        difference = x - self.x
        self.real_x += difference
        self.x = x
        self.y = y

    def get_pos(self):
        return (self.x,self.y)

    def update(self, t, width, height, cam_speed):
        #velocity
        self.dx += self.ddx
        self.dy += self.ddy
        if self.dx < 0: self.dx = 0
        
        # postion
        self.x += self.dx - cam_speed[0]
        self.y -= self.dy - cam_speed[1]
        
        #real position (according to the init of the level)
        self.real_x += self.dx
        
        self.rect = Rect(self.real_x, self.y, self._w, self._h)
        #print "Real  ", self.rect
        #print "Relative", self.get_pos()
        
        #emulate gravity
        self.ddy = -0.15
        
        #adds falling time
        if self.falling:
            self.falling_time += 1
        
        if self.onGround == False:
        	if self.dy == 0 or \
        	self.dy - self.ddy > 0 and self.dy < 0:
        	    print self.falling_time
        	    self.falling = True
        	        
        #Changes sprite case its falling too high
        if self.falling_time > 55:
            self.tooHigh = True
            
        #count sprinting time
        if self.sprint_timeout <= 0 and self.sprinting:
            self.sprinting = False
            print 'stoooop'
            self.animation_key = "running"
        elif self.sprinting:
            time_passed = t - self._last_update
            print self.sprint_timeout
            self.sprint_timeout -= time_passed
        
        # animation
        self.animate[self.animation_key](t)

    def stop(self):
    	self.ddx = 0
        self.dx = 0
    
    
    #FIXME: Essa colisao nao esta boa, pq ela esta checando colisao de rect do sprite com os rects dos objetos. 
    #Seria legal se fosse colisao de pixel do sprite com os rects dos objetos
        
    # Receives the 'ground' or 'killer' list (of 4-uples) from Game.py and returns:
    # -1, -1: if there's no collision at all
    # obj, 1: if the sprite collides with the object from the top
    # obj, 2: if the sprite collides with the object from the left
    def collides_with_objects(self, objects_list):
        for obj in objects_list:

            if self.rect.colliderect(Rect(obj)):
                return obj, 1
        return -1, -1



    def put_on_ground_running(self, ground_y):
        self.dy = 0
        self.ddy = 0
        #self.animation_key = "running"
        self.y = ground_y - self._h
        self.forceJump = 2
        if not self.onGround:
            self.onGround = True
            self.animation_key = "running"
        self.falling = False
        self.falling_time = 0
        if self.tooHigh:
            self.tooHigh = False
            if self.pendingRoll == False:
                #quebrou as pernas
                self.stop()
        if self.pendingRoll:
            self.doRoll()
            self.pendingRoll = False

    def doJump(self):

        if self.onGround:
            self.animation_key = "jumping"
            self.onGround = False
            self.dy = 8
            self.ddy = -0.05
    def stopJump(self):
        if self.dy > 0:
            self.dy /= 2;
            
    def doRoll(self):
        if self.onGround:
            print 'ROLLLLLLLLLLLLLLLL!'
            #self.animation_key = "rolling"
            
    def doGetDown(self):
        if self.onGround:
            self.mask = pygame.mask.from_surface(self._framelist[10])
            self. ddx = -0.02
            self.animation_key = "getting_down"
    def stopGetDown(self):
        if self.onGround:
            self.mask = pygame.mask.from_surface(self._framelist[0])
            self. ddx = 0
            self.animation_key = "running"
    
    def doSprint(self):
        if self.onGround:
            self.sprinting = True
            self.sprint_timeout = 1500
            self.animation_key = "sprinting"
            self.dx += 1
            #self.animation_key = "rolling"
            
#    def doSprint():
#    def doGetDown():
#    def doClimb():

    def _anim_run(self, t):
	    if t - self._last_update > self._delay:
	        self._frame += 1
	        if self._frame >= 9:
		    self._frame = 0
	        if self.onGround:
		        self.image = self._framelist[self._frame]
	        self._last_update = t
	        
    def _anim_sprint(self, t):
	    if t - self._last_update > self._delay:
	        self._frame += 2
	        if self._frame >= 9:
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
	    
    def _anim_get_down(self, t):
	    self.image = self._framelist[10]
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
