import pygame
from pygame.locals import *

import sys, os
from tmx_loader import TileMapParser, ImageLoaderPygame, set_slices, get_ground_objects, get_killer_objects

from xml import sax
from Obstacle import *

from Map import TMXHandler
from Map import Tileset

from Command import *

from Caracter import *

def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True

    #Constantes
    FASE_TIMEOUT = 40000
    SLICE_SIZE_PIXEL = 5120
    SLICE_SIZE = 80
    REPEAT_DELAY = 50 #milisseconds between each KEYDOWN event (when repeating)
    KEY_TIMEOUT = 230 #MAX milisseconds between key pressings
    SCREEN_WIDTH, SCREEN_HEIGHT = (1024,  768)
    
    fase_timeout = FASE_TIMEOUT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Good Intentions")
    font = pygame.font.Font(os.path.join('', 'data', 'actionj.ttf'), 80)
    font_small = pygame.font.Font(os.path.join('', 'data', 'actionj.ttf'), 35)
    km_label_text = font_small.render('Km/h', 1, (15,15,215))
    pygame.mixer.music.load(os.path.join('', 'sounds', 'beep.mp3'))
    time_display = pygame.image.load(os.path.join('', 'images', 'display.png'))
    img_fatguy = pygame.image.load(os.path.join('', 'images', 'sprite.png'))
    fatguy = Caracter("jonatas", img_fatguy, 10, 115, 115, 25)
    commandHandler = CommandHandler(fatguy)
    cam_speed  = (6,0)
    
    fatguy.set_pos(150,525)
    
    
    world_map = TileMapParser().parse_decode("huge_objects.tmx")
    world_map.load(ImageLoaderPygame())
    
    ground_objects = get_ground_objects(world_map)
    killer_objects = get_killer_objects(world_map)
    slices = set_slices(world_map, SLICE_SIZE, SLICE_SIZE_PIXEL)

    key_timeout = -1

    #create sprites groups for collision detection
    playerGroup = pygame.sprite.RenderUpdates()
    playerGroup.add(fatguy)

    objectGroup = pygame.sprite.Group()
    enemyGroup = pygame.sprite.Group()
    sceneGroup = pygame.sprite.Group()

    
    offset = 0
    actual_slice = slices.pop(0)
    secs = int((fase_timeout) / 1000)
    past_slice = actual_slice
    transition = False
    while running:

        clock.tick(90)
        ob = ground_objects[0]
        if ob[0] + ob[2] <= fatguy.real_x:
        	ground_objects.pop(0)
        
        #blit level----------------------------------------------------------------------------------
        if transition:
            join_point = SLICE_SIZE_PIXEL - offset
            screen.blit(past_slice.subsurface(offset, 0, join_point, SCREEN_HEIGHT),(0,0))
            screen.blit(actual_slice.subsurface(0 ,0, (offset + SCREEN_WIDTH - SLICE_SIZE_PIXEL), SCREEN_HEIGHT),(join_point,0))
            if join_point < 0:
                offset = 0
                transition = False
        else:
            screen.blit(actual_slice.subsurface((offset,0,SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        
        offset += cam_speed[0]
        if(offset + SCREEN_WIDTH) > SLICE_SIZE_PIXEL and transition == False:
            past_slice = actual_slice
            if len(slices) == 0: break
            actual_slice = slices.pop(0)
            transition = True
        #----------------------------------------------------------------------------------------------
	    
	#bliting HUD
        secs_before = secs
        secs = int((fase_timeout - pygame.time.get_ticks()) / 1000)
        decs = int(((fase_timeout -pygame.time.get_ticks()) % 1000) / 10)
        
        if secs < 10:
            if secs_before > secs:
                pygame.mixer.music.play(0, 0)
            timeup_text = font.render('0' + str(secs) + ':' + str(decs), 1, (200,5,15))
        else:
            timeup_text = font.render(str(secs) + ':' + str(decs), 1, (160,200,180))
        screen.blit(time_display, (730,-3))
        screen.blit(timeup_text, Rect(785, 7, 300, 90))
        
        speed_m_per_s = float(fatguy.dx / 64.0) * 100
        speed_km_per_h = int(speed_m_per_s * 3.6)
        speed_text = font.render(str(speed_km_per_h), 1, (15,15,215))
        screen.blit(speed_text, Rect(765, 680, 300, 90))
        screen.blit(km_label_text, Rect(865, 690, 300, 90))
        #-------------------------------------------------------------------------------
	    
        screen.blit(fatguy.image,  fatguy.get_pos())
        obj, col_type = fatguy.collides_with_objects(killer_objects)
        if col_type == 1:
            if pygame.sprite.collide_mask(fatguy, obj):
                fatguy.stop()
            
        fatguy.update(pygame.time.get_ticks(), SCREEN_WIDTH, SCREEN_HEIGHT, cam_speed)
        
        obj, col_type = fatguy.collides_with_objects(ground_objects)
        if  col_type == 1:
            fatguy.put_on_ground_running(obj[1])
        

        if key_timeout >= 0:
            if (pygame.time.get_ticks() - key_timeout) > KEY_TIMEOUT:
                commandHandler.actual_state = 0
                key_timeout = -1
        adjust = 0
        if fatguy.sprinting:
            adjust = -4
        if fatguy.x > 100:
            adjust += 2
        else:
            adjust = 0
        cam_speed = (fatguy.dx + adjust,0)
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                running = False
            elif e.type == KEYDOWN:
                key_timeout = pygame.time.get_ticks()
                fatguy.state = commandHandler.refresh_state(e.key)
            elif e.type == KEYUP:
            	if e.key == K_UP:
                    fatguy.stopJump()
                if e.key == K_DOWN:
                    if not fatguy.onGround:
                        fatguy.pendingGetDown = False
                    else: fatguy.stopGetDown()
            if not fatguy.alive():
                print 'Game Over'
                pygame.time.wait(2000)
                sys.exit()
#        pygame.display.update()
        pygame.display.flip()
#        pygame.time.delay(10)

if __name__ == "__main__": main()
