import pygame
from pygame.locals import *

import sys, os
from tmx_loader import TileMapParser, ImageLoaderPygame, set_slices, get_ground_objects, get_killer_objects, get_checkpoint_objects

from xml import sax
from Obstacle import *

from Map import TMXHandler
from Map import Tileset

from Command import *

from Caracter import *

# Slice attributes
SLICE_SIZE_PIXEL = 5120 
SLICE_SIZE = 80
# Milisseconds between each KEYDOWN event (when repeating)
REPEAT_DELAY = 50 
# MAX milisseconds between key pressings
KEY_TIMEOUT = 230 
# Screen resolution
SCREEN_WIDTH, SCREEN_HEIGHT = (1024,  768)
RESET_DELAY = 30

# Main Class of the game
class Game:

    def __init__(self,stage_path,fase_timeout=40000, fatguy_x=150, fatguy_y=525):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fase_timeout = fase_timeout
        
        # Loading content...
        pygame.display.set_caption("Good Intentions")
        self.font = pygame.font.Font(os.path.join('', 'data', 'actionj.ttf'), 80)
        self.font_small = pygame.font.Font(os.path.join('', 'data', 'actionj.ttf'), 35)
        self.km_label_text = self.font_small.render('Km/h', 1, (15,15,215))
        pygame.mixer.music.load(os.path.join('', 'sounds', 'beep.mp3'))
        self.time_display = pygame.image.load(os.path.join('', 'images', 'display.png'))
        self.img_fatguy = pygame.image.load(os.path.join('', 'images', 'sprite.png'))
        
        # Loading Rolando 
        self.fatguy = Caracter("Rolando", self.img_fatguy, 10, 115, 115, 25)
        self.commandHandler = CommandHandler(self.fatguy)
        self.fatguy.set_pos(fatguy_x,fatguy_y)
        self.dead = False
        self.fatguy_x = fatguy_x
        self.fatguy_y = fatguy_y
        
        # Initial Speed of the camera
        self.cam_speed  = (6,0)
        
        # Loading the stage
        self.world_map = TileMapParser().parse_decode(stage_path)
        self.world_map.load(ImageLoaderPygame())
    
        # Creating list of collision objects 
        self.ground_objects = get_ground_objects(self.world_map)
        self.killer_objects = get_killer_objects(self.world_map)
        self.checkpoint_objects = get_checkpoint_objects(self.world_map)
        
        self.slices = set_slices(self.world_map, SLICE_SIZE, SLICE_SIZE_PIXEL)
        self._slices = set_slices(self.world_map,SLICE_SIZE,SLICE_SIZE_PIXEL)
        self.key_timeout = -1

        # Create sprites groups for collision detection
        self.playerGroup = pygame.sprite.RenderUpdates()
        self.playerGroup.add(self.fatguy)

        self.objectGroup = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()
        self.sceneGroup = pygame.sprite.Group()
        
        # Controlling the movement of the background
        self.offset = 0
        self.actual_slice = self.slices.pop(0)
        self.secs = int((self.fase_timeout) / 1000)
        self.past_slice = self.actual_slice
        self.transition = False
        
        # Controlling the reset
        self.reset_delay = RESET_DELAY

    # The main function of the class
    def main_loop(self):

        while self.running:
            self.clock.tick(90)
#            self.recicle()
            self.draw_background()
            self.draw_hud()
            self.update_fatguy()
            self.draw_fatguy()
            self.event_handler()
            
            
    
    def recicle(self):
        g_object = self.ground_objects[0]
        k_object = self.killer_objects[0]
        c_object = self.checkpoint_objects[0]
        
        if g_object[0] + g_object[2] <= self.fatguy.real_x:
            self.ground_objects.pop(0)
            
        if k_object.rect.x + k_object.rect.width < self.fatguy.real_x:
            self.killer_objects.pop(0)
            
        if c_object[0] + c_object[2] <= self.fatguy.real_x:
            self.checkpoint_objects.pop(0)
       
            
    def draw_background(self):
        if self.transition:
            join_point = SLICE_SIZE_PIXEL - self.offset
            self.screen.blit(self.past_slice.subsurface(self.offset, 0, join_point, SCREEN_HEIGHT),(0,0))
            self.screen.blit(self.actual_slice.subsurface(0 ,0, (self.offset + SCREEN_WIDTH - SLICE_SIZE_PIXEL), SCREEN_HEIGHT),(join_point,0))
            if join_point < 0:
                self.offset = 0
                self.transition = False
        else:
            self.screen.blit(self.actual_slice.subsurface((self.offset,0,SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        
        self.offset += self.cam_speed[0]
        if(self.offset + SCREEN_WIDTH) > SLICE_SIZE_PIXEL and self.transition == False:
            self.past_slice = self.actual_slice
            if len(self.slices) == 0: return
            self.actual_slice = self.slices.pop(0)
            self.transition = True

    def draw_hud(self):      
        secs_before = self.secs
        self.secs = int((self.fase_timeout - pygame.time.get_ticks()) / 1000)
        decs = int(((self.fase_timeout -pygame.time.get_ticks()) % 1000) / 10)
        
        if self.secs < 10:
#            if secs_before > self.secs:
#                pygame.mixer.music.play(0, 0)
            timeup_text = self.font.render('0' + str(self.secs) + ':' + str(decs), 1, (200,5,15))
        else:
            timeup_text = self.font.render(str(self.secs) + ':' + str(decs), 1, (160,200,180))
        self.screen.blit(self.time_display, (730,-3))
        self.screen.blit(timeup_text, Rect(785, 7, 300, 90))
        
        speed_m_per_s = float(self.fatguy.dx / 64.0) * 100
        speed_km_per_h = int(speed_m_per_s * 3.6)
        speed_text = self.font.render(str(speed_km_per_h), 1, (15,15,215))
        self.screen.blit(speed_text, Rect(765, 680, 300, 90))
        self.screen.blit(self.km_label_text, Rect(865, 690, 300, 90))
            
    def draw_fatguy(self):
        self.screen.blit(self.fatguy.image,  self.fatguy.get_pos())
        
    def update_fatguy(self):
        # Collides with Killer Objects
        obj, col_type = self.fatguy.collides_with_objects(self.killer_objects)
        if col_type == 1:
            if not self.dead:
                if pygame.sprite.collide_mask(self.fatguy, obj):
                    self.fatguy.doCrashSide(obj.rect.x)
                    self.fatguy.sprinting = False
                    self.fatguy.onGround = True
                    self.dead = True
                
#            if pygame.sprite.collide_mask(self.fatguy, obj):
#                self.fatguy.stop()
             
             
        self.fatguy.update(pygame.time.get_ticks(), SCREEN_WIDTH, SCREEN_HEIGHT, self.cam_speed)
        
        # Collides with the ground
        obj, col_type = self.fatguy.collides_with_objects(self.ground_objects)
        if  col_type == 1:
            self.fatguy.put_on_ground_running(obj[1])

        # Collides with the checkpoint 
        check_obj, check_collision = self.fatguy.collides_with_objects(self.checkpoint_objects)
#        if check_collision == 1:
#            self.fatguy_x = check_obj[0]
        
        if self.key_timeout >= 0:
            if (pygame.time.get_ticks() - self.key_timeout) > KEY_TIMEOUT:
                self.commandHandler.actual_state = 0
                self.key_timeout = -1
                
        adjust = 0
        
        if not self.dead:
            if self.fatguy.sprinting:
                adjust = -4
            if self.fatguy.x > 100:
                adjust += 2
            else:
                adjust = 0
            self.cam_speed = (self.fatguy.dx + adjust,0)
        else:
            self.reset_delay -= 1
            if self.reset_delay == 0:
                self.reset()
                self.reset_delay = RESET_DELAY
            
    def event_handler(self):
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                self.running = False
            elif e.type == KEYDOWN:
                self.key_timeout = pygame.time.get_ticks()
                self.fatguy.state = self.commandHandler.refresh_state(e.key)
            elif e.type == KEYUP:
            	if e.key == K_UP:
                    self.fatguy.stopJump()
                if e.key == K_DOWN:
                    if not self.fatguy.onGround:
                        self.fatguy.pendingGetDown = False
                    else: self.fatguy.stopGetDown()
            if not self.fatguy.alive():
                self.game_over()
                pygame.time.wait(2000)
                sys.exit()
        pygame.display.flip()
        
        
    def reset(self):
        alpha = 0
        fill_surf = pygame.Surface((1024,768))
        fill_surf.fill((10,10,10))
        
        # Escurece a tela
        while alpha < 255:
            self.clock.tick(20)
            alpha+=15
            fill_surf.set_alpha(alpha)
            self.screen.blit(fill_surf, (0,0))
            pygame.display.flip()

        self.fatguy = Caracter("Rolando", self.img_fatguy, 10, 115, 115, 25)
        self.fatguy.set_pos(self.fatguy_x,self.fatguy_y)
        self.dead = False
        
        self.offset = 0
        self.slices = self._slices
        self.actual_slice = self.slices.pop(0)
        self.secs = int((self.fase_timeout) / 1000)
        self.past_slice = self.actual_slice
        self.transition = False


        # Mostra a tela
        while alpha > 0:
            self.clock.tick(20)
            alpha-=15
            fill_surf.set_alpha(alpha)
            self.screen.blit(fill_surf, (0,0))
#            self.screen.blit(self.actual_slice.subsurface((self.offset,0,SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
            pygame.display.flip()
            

        
    
    def game_over(self):
        self.fatguy.lifes -= 1
        if self.fatguy.lifes > 0:
            self.fatguy.set_pos(self.fatguy_x,self.fatguy_y)
        
        
        
def game_main():
    game = Game("huge_objects.tmx")        
    game.main_loop()

if __name__ == "__main__": game_main()
