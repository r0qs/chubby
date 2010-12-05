import pygame
from pygame.locals import *

from Menu import *

import sys, os
from Tmx_loader import TileMapParser, ImageLoaderPygame, set_slices, get_ground_objects, get_killer_objects, get_checkpoint_objects

from xml import sax
from Obstacle import *

from random import randrange, random

from Command import *

from Caracter import *

from Sound import *

from Story import Story 

# Slice attributes
SLICE_SIZE_PIXEL = 5120 
SLICE_SIZE = 80
# Milisseconds between each KEYDOWN event (when repeating)
REPEAT_DELAY = 50 
# MAX milisseconds between key pressings
KEY_TIMEOUT = 230 
# Screen resolution
SCREEN_WIDTH, SCREEN_HEIGHT = (1024,  768)
# Delay to reset a stage
RESET_DELAY = 50

# Main Class of the game
class Game:

    def __init__(self,stage_path,fase_timeout, fatguy_x, fatguy_y, music):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.initial_clock = pygame.time.get_ticks()
        self.running = True

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fase_timeout = fase_timeout
        self.shake = (0,0)
        self.shake_amplitude = 10
        # Loading content...
        pygame.display.set_caption("Good Intentions")
        self.font = pygame.font.Font(os.path.join('', 'data', 'actionj.ttf'), 70)
        self.font_small = pygame.font.Font(os.path.join('', 'data', 'actionj.ttf'), 28)
        self.km_label_text = self.font_small.render('Km/h', 1, (200,205,215))
        self.time_display = pygame.image.load(os.path.join('', 'images', 'display.png'))
        self.speed_display = pygame.image.load(os.path.join('', 'images', 'display_speed.png'))
        self.img_fatguy = pygame.image.load(os.path.join('', 'images', 'sprite.png'))
        
        #Sounds
        self.bg_music = Music()
        self.bg_music.load_music(music)
        self.beep = SoundEffect()

        # Loading Rolando 
        self.fatguy = Caracter("Rolando", self.img_fatguy, 10, 115, 115, 25)
        self.fatguy.set_pos(fatguy_x,fatguy_y)
        self.commandHandler = CommandHandler(self.fatguy)
        self.dead = False
        self.fatguy_x = fatguy_x
        self.fatguy_y = fatguy_y
        
        # Initial Speed of the camera
        self.cam_speed  = (70,0)
        
        # Loading the stage
        self.world_map = TileMapParser().parse_decode(stage_path)
        self.world_map.load(ImageLoaderPygame())
    
        # Creating list of collision objects 
        self.ground_objects = get_ground_objects(self.world_map)
        self.killer_objects = get_killer_objects(self.world_map)
        self.checkpoint_objects = get_checkpoint_objects(self.world_map)
        
        self.slices = set_slices(self.world_map, SLICE_SIZE, SLICE_SIZE_PIXEL)
        self.initialize_slices()
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
    
    # Calcule the first slice of the stage
    def initialize_slices(self):
        flag = False
        x = self.fatguy_x
        real_x = SLICE_SIZE_PIXEL
        while(x > SLICE_SIZE_PIXEL):
            g_object = self.ground_objects[0]
            k_object = self.killer_objects[0]
            c_object = self.checkpoint_objects[0]
            while(g_object[0] + g_object[2] < real_x):
                self.ground_objects.pop(0)
                g_object = self.ground_objects[0]
          #  while(k_object[0] + k_object[2] < real_x):
          #      self.killer_objects.pop(0)
          #      k_object = self.killer_objects[0]
            while(c_object[0] + c_object[2] < real_x):
                self.checkpoint_objects.pop(0)
                c_object = self.checkpoint_objects[0]
            self.slices.pop(0)
            real_x += SLICE_SIZE_PIXEL
            x -= SLICE_SIZE_PIXEL
            flag = True
        self.offset = x 

    # The main function of the class
    def main_loop(self):
        self.bg_music.play_load_music(1)
        while self.running:
            self.clock.tick(90)
            self.recicle()
            self.draw_background()
            self.draw_hud()
            self.update_fatguy()
            self.killer_collision()
            self.ground_collision()
            self.checkpoint_collision()
            self.draw_fatguy()
            self.event_handler()
        self.bg_music.pause_music()
        # Return the position of Rolando
        return self.fatguy_x, self.fatguy_y

    # Throw away utilized objects
    def recicle(self):
        g_object = self.ground_objects[0]
        k_object = self.killer_objects[0]
        c_object = self.checkpoint_objects[0]
        
        if g_object[0] + g_object[2] <= self.fatguy.real_x:
            self.ground_objects.pop(0)
            
        if k_object.rect.x + k_object.rect.width < self.fatguy.real_x:
            self.killer_objects.pop(0)
            
        if c_object[0] <= self.fatguy.real_x:
            self.checkpoint_objects.pop(0)
       
    # Calcule and Draw the Background  
    def draw_background(self):
        if self.transition:
            join_point = SLICE_SIZE_PIXEL - self.offset
            self.screen.blit(self.past_slice.subsurface(self.offset, 0, join_point, SCREEN_HEIGHT),self.shake)
            self.screen.blit(self.actual_slice.subsurface(0 ,0, (self.offset + SCREEN_WIDTH - SLICE_SIZE_PIXEL), SCREEN_HEIGHT),(join_point + self.shake[0],self.shake[1]))
            if join_point < 0:
                self.offset = 0
                self.transition = False
        else:
            self.screen.blit(self.actual_slice.subsurface((self.offset,0,SCREEN_WIDTH, SCREEN_HEIGHT)), self.shake)
        
        self.offset += self.cam_speed[0]
        if(self.offset + SCREEN_WIDTH) > SLICE_SIZE_PIXEL and self.transition == False:
            self.past_slice = self.actual_slice
            if len(self.slices) == 0: 
                return None
            self.actual_slice = self.slices.pop(0)
            self.transition = True
        
            
    # Draw the head's up display
    def draw_hud(self):      
        secs_before = self.secs
        time = int(self.fase_timeout - (pygame.time.get_ticks() - self.initial_clock))
        self.secs = time / 1000
        decs = ((time % 1000) / 10)

        if self.secs < 10:
            if secs_before > self.secs:
               self.beep.play_effect('beep.ogg', 1, 0)
            timeup_text = self.font.render('0' + str(self.secs) + ':' + str(decs), 1, (200,5,15))
        else:
            timeup_text = self.font.render(str(self.secs) + ':' + str(decs), 1, (160,200,180))
        self.screen.blit(self.time_display, (730,-3))
        self.screen.blit(timeup_text, Rect(785, 7, 300, 90))
        
        speed_m_per_s = float(self.fatguy.dx / 64.0) * 100
        speed_km_per_h = int(speed_m_per_s * 3.6)
        speed_text = self.font.render(str(speed_km_per_h), 1, (200,205,215))
        self.screen.blit(self.speed_display, (788,668))
        self.screen.blit(speed_text, Rect(820, 690, 300, 90))
        self.screen.blit(self.km_label_text, (930, 682))
            
    # Draw the fatguy
    def draw_fatguy(self):
        self.screen.blit(self.fatguy.image,  self.fatguy.get_pos())
        
    # Update the fatguy's variables and change his animation
    def update_fatguy(self):
        self.fatguy.update(pygame.time.get_ticks(), SCREEN_WIDTH, SCREEN_HEIGHT, self.cam_speed)
        if self.key_timeout >= 0:
            if (pygame.time.get_ticks() - self.key_timeout) > KEY_TIMEOUT:
                self.commandHandler.actual_state = 0
                self.key_timeout = -1
                
        adjust = 0
        #check if the Fatguy's too high
        if self.fatguy.falling and self.ground_objects[0][1] - self.fatguy.apex_height > 335:
           print self.fatguy.apex_height, self.ground_objects[0][1]
           self.fatguy.doTooHigh()
        
        if not self.dead:
            if self.fatguy.sprinting:
                adjust = -4
            if self.fatguy.x > 150:  ##
                adjust += 2
            else:
                adjust = 0
            self.cam_speed = (self.fatguy.dx + adjust,0)
        else:
            self.reset_delay -= 1
            if self.reset_delay == 0:
                fade_out(self.screen,self.clock)
                self.running = False
        
    # Collides with Killer Objects
    def killer_collision(self):
        obj, col_type = self.fatguy.collides_with_objects(self.killer_objects)
        if col_type == 1:
            if not self.dead:
                if pygame.sprite.collide_mask(self.fatguy, obj):
                    self.fatguy.doCrashSide(obj.rect.x)
                    self.fatguy.sprinting = False
                    self.fatguy.onGround = True
                    self.dead = True
            else:
                if self.shake_amplitude > 0:
                    self.shake = (randrange(-self.shake_amplitude,self.shake_amplitude),randrange(-self.shake_amplitude,self.shake_amplitude) + random())
                    self.shake_amplitude -= 1
                    
    # Collides with the ground
    def ground_collision(self):
        obj, col_type = self.fatguy.collides_with_objects(self.ground_objects)
        if  col_type == 1:
            self.fatguy.put_on_ground_running(obj[1])
            
    # Collides with the checkpoint 
    def checkpoint_collision(self):
        check_obj, check_collision = self.fatguy.collides_with_objects(self.checkpoint_objects)
        if check_collision == 1:
            self.fatguy_x = check_obj[0]
            self.fatguy_y = check_obj[1] + check_obj[3]


            
    def event_handler(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            elif (e.type == KEYDOWN and e.key == K_ESCAPE):
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
                    if self.fatguy.sliding: self.fatguy.stopGetDown()
            if not self.fatguy.alive():
                self.game_over()
                pygame.time.wait(2000)
                sys.exit()
        pygame.display.flip()
        
        
def fade_out(screen,clock):
    fill_surf = pygame.Surface((1024,768))
    fill_surf.fill((10,10,10))
    alpha = 0
    while alpha < 255:
        clock.tick(20)
        alpha+=10
        fill_surf.set_alpha(alpha)
        screen.blit(fill_surf, (0,0))
        pygame.display.flip()
        
def set_game_over_menu():
    width = 1024
    height = 768
    pygame.display.init
    menu_screen = pygame.display.set_mode((width,height))
    # Background
    background = pygame.image.load(os.path.join('', 'images', 'game_over_bg.jpg'))
    background = background.convert()

    # Cursor
    pygame.mouse.set_visible(False)
    cursor = Cursor(16,16,'images/cursor.png')

    #Options in menu
    retry = Option(100,200,550,61,'images/retry.png','images/retry_big.png',game_main, 1.109,0.05)
    quit = Option(100,270,274,60,'images/quit.png','images/quit_big.png',sys.exit, 1.11,0.05)

    # Menu
    menu = Menu()
    menu.append(retry)
    menu.append(quit)

    menu_screen.blit(background, (0, 0))
    cursor.draw(menu_screen)
    menu.draw(menu_screen)
    pygame.display.flip()

    # Event loop
    while 1:
        menu.update(cursor)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit
                sys.exit()
                return
            elif event.type == MOUSEMOTION:
                pygame.mouse.get_pos()
                cursor.update()
            elif event.type == MOUSEBUTTONDOWN:
                menu.activate()
        menu_screen.blit(background, (0, 0))
        menu.draw(menu_screen)
        cursor.draw(menu_screen)
        pygame.display.flip()
        
        
def game_main():
    prolog_music = Music()
    prolog_music.play_music('Gluck-Melodie-Orfeo-ed-Euridice-1951-2.ogg',1)
    prolog = Story('prologo01', 6)
    prolog.play()
    prolog_music.fadeout_music(1)
    game = Game("huge_objects.tmx",200000,150,525,'Dicennian_Running_Past.ogg')
    posx, posy = game.main_loop()
    print("POSICAO NO FINAL")
    print(posx ,posy)
    game2 = Game("huge_objects.tmx",200000,posx,posy,'CorvusCorax-Tourdion.ogg')
    game2.main_loop()
    game_over_menu = set_game_over_menu()

if __name__ == "__main__": game_main()
