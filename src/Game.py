import pygame
from pygame.locals import *

import sys, os
from tmx_loader import TileMapParser, ImageLoaderPygame, set_slices

from xml import sax

from Map import TMXHandler
from Map import Tileset

from Command import *

from Caracter import *

def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True

    #Constantes
    SLICE_SIZE_PIXEL = 5120
    SLICE_SIZE = 80
    REPEAT_DELAY = 30 #milisseconds between each KEYDOWN event (when repeating)
    KEY_TIMEOUT = 185 #MAX milisseconds between key pressings
    SCREEN_WIDTH, SCREEN_HEIGHT = (1024, 640)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Good Intentions")
    img_fatguy = pygame.image.load(os.path.join('', 'images', 'sprite.png'))
    fatguy = Caracter("jonatas", img_fatguy, 10, 115, 115, 25)
    commandHandler = CommandHandler(fatguy)
    
    fatguy.set_pos(200,205)
    fatguy.dx = 0
    fatguy.dy = 5
    fatguy.ddy = -0.15
    
    
    world_map = TileMapParser().parse_decode("huge.tmx")
    world_map.load(ImageLoaderPygame())
    
    slices = set_slices(world_map, SLICE_SIZE, SLICE_SIZE_PIXEL)

    key_timeout = -1

    #create sprites groups for collision detection
    playerGroup = pygame.sprite.RenderUpdates()
    playerGroup.add(fatguy)

    objectGroup = pygame.sprite.Group()
    enemyGroup = pygame.sprite.Group()
    sceneGroup = pygame.sprite.Group()

    pygame.key.set_repeat(REPEAT_DELAY*3, REPEAT_DELAY)
    
    offset = 0
    actual_slice = slices.pop(0)
    past_slice = actual_slice
    transition = False
    while running:
        clock.tick(90)

        if fatguy.y > 205:
            fatguy.animation_key = "running" 
            fatguy.y = 205
            fatguy.ddy = 0
            fatguy.dy = 0        
                
        if transition:
            join_point = SLICE_SIZE_PIXEL - offset
            screen.blit(past_slice.subsurface(offset, 0, join_point, SCREEN_HEIGHT),(0,0))
            screen.blit(actual_slice.subsurface(0 ,0, (offset + SCREEN_WIDTH - SLICE_SIZE_PIXEL), SCREEN_HEIGHT),(join_point,0))
            if join_point < 0:
                offset = 0
                transition = False
        else:
            screen.blit(actual_slice.subsurface((offset,0,SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        
        offset += 4
        if(offset + SCREEN_WIDTH) > SLICE_SIZE_PIXEL and transition == False:
            past_slice = actual_slice
            if len(slices) == 0: break
            actual_slice = slices.pop(0)
            transition = True

        screen.blit(fatguy.image,  fatguy.get_pos())
        fatguy.update(pygame.time.get_ticks(), SCREEN_WIDTH, SCREEN_HEIGHT)

        if key_timeout >= 0:
            if (pygame.time.get_ticks() - key_timeout) > KEY_TIMEOUT:
                commandHandler.actual_state = 0
                key_timeout = -1

        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                running = False
            elif e.type == KEYDOWN:
                key_timeout = pygame.time.get_ticks()
                fatguy.state = commandHandler.refresh_state(e.key)
            if not fatguy.alive():
                print 'Game Over'
                pygame.time.wait(2000)
                sys.exit()

#        pygame.display.update()
        pygame.display.flip()
#        pygame.time.delay(10)

if __name__ == "__main__": main()
