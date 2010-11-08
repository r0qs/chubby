import pygame
from pygame.locals import *

import sys, os

from xml import sax

from Map import TMXHandler
from Map import Tileset

from Command import *

from Caracter import *

def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True
    
    commandHandler = CommandHandler()

    #Constantes
    REPEAT_DELAY = 30 #milisseconds between each KEYDOWN event (when repeating)
    KEY_TIMEOUT = 185 #MAX milisseconds between key pressings
    SCREEN_WIDTH, SCREEN_HEIGHT = (640, 480)

    screen_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Good Intentions")
    img_fatguy = pygame.image.load(os.path.join('', 'images', 'fat.png'))
    fatguy = Caracter("jonatas", img_fatguy, 10, 115, 115, 25)
#    fatguy.set_pos(0,240)
    fatguy.set_pos(0,325)

    parser = sax.make_parser()
    tmxhandler = TMXHandler()
    parser.setContentHandler(tmxhandler)
    parser.parse("grande.tmx")

    key_timeout = -1

    #create sprites groups for collision detection
    playerGroup = pygame.sprite.RenderUpdates()
    playerGroup.add(fatguy)

    objectGroup = pygame.sprite.Group()
    enemyGroup = pygame.sprite.Group()
    sceneGroup = pygame.sprite.Group()

    pygame.key.set_repeat(REPEAT_DELAY*3, REPEAT_DELAY)
    while running:
        clock.tick(30)

        screen_surface.fill((255,255,255))

        screen_surface.blit(tmxhandler.image, (0,0))
        tmxhandler.image.scroll(-10,0)

        screen_surface.blit(fatguy.image,  fatguy.get_pos())
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
