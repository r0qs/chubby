import pygame
from pygame.locals import *

import sys
# Global Variable that define tha actual stage of he player
#actual_stage = 0

class Option:

    # selected_size = the size of the surface when she's selected (2 = double size)
    # resize_frame = how larger/small one surface can be in one iteration (0.13 = 13%)
    # function = the function assigned to a option. The function need to be implemented ...(obvious xD)
    def __init__(self,x,y,width,height,image_path,big_image_path,function,selected_size=2,resize_frame=0.10,opened=True):
        self.x = x
        self.y = y
        self.center = x+width/2,y+height/2
        self._width = width
        self._height = height
        self.width = width
        self.max_width = width*selected_size
        self.resize_frame = resize_frame
        self.height = height
        self.image = pygame.image.load(image_path)
        self.little_image = self.image.copy()
        self.big_image = pygame.image.load(big_image_path)
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.function = function
        self.selected = False
        self.change_image = False
        self.opened = opened
        
    def mouse_on(self):
        self.selected = True
        if self.width < self.max_width:
            self.image = pygame.transform.scale(self.image,(self.width*(1+self.resize_frame),self.height*(1+self.resize_frame)))
            self.change_image = False
        else:
            if not self.change_image:
                self.change_image = True
                self.image = self.big_image.copy()
        self.width , self.height = self.image.get_size()
        self.rect = self.image.get_rect(center=(self.center)) 
            
        
            
    def mouse_off(self):
        self.selected = False
        if self.width > self._width:
            self.image = pygame.transform.scale(self.image,(self.width*(1-self.resize_frame),self.height*(1-self.resize_frame)))
            self.change_image = False
        else:
            if not self.change_image:
                self.change_image = True
                self.image = self.little_image.copy()
        self.width , self.height = self.image.get_size()
        self.rect = self.image.get_rect(center=(self.center))
        
    
    def get_rect(self):
        return self.rect
        
    def activate(self):
        if self.selected:
            actual_stage = self.function()
            
        
    def draw(self,screen):
        screen.blit(self.image,self.rect)

class Cursor:
    def __init__(self,width,height,image_path):
        self.width = width
        self.height = height
        self.x , self.y = pygame.mouse.get_pos()
        self.image = pygame.image.load(image_path)
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.rect.width = 5
        self.rect.height = 5
        
    def update(self):
        self.x , self.y = pygame.mouse.get_pos()
        self.rect.left = self.x
        self.rect.top = self.y
        
    def draw (self,screen):
        screen.blit(self.image,self.rect)
        
    def on_option(self,option):
        menu_rect = option.get_rect()
        return self.rect.colliderect(option)
        
    def select(self,option):
        option.is_Selected = True

class Menu:
    def __init__(self):
        self.options = []
    
    def append(self,option):
        self.options.append(option)
            
    def update(self,cursor):
        for option in self.options:
            if option.opened:
                if cursor.on_option(option):
                    option.mouse_on()
                    
                else:
                    option.mouse_off()
                
    def draw(self,screen):
        for option in self.options:
            option.draw(screen)
            
    def activate(self):
        for option in self.options:
            option.activate()
            
            
    def main_loop(self,cursor,menu_screen,background):
        while True:
            self.update(cursor)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False
                    return
                elif event.type == MOUSEMOTION:
                    pygame.mouse.get_pos()
                    cursor.update()
                elif event.type == MOUSEBUTTONDOWN:
                    self.activate()

            menu_screen.blit(background, (0, 0))
            self.draw(menu_screen)
            cursor.draw(menu_screen)
            pygame.display.flip()
    
