import pygame
from pygame.locals import *
from sys import exit


from commands import *
from Command import *

pygame.init()
clock = pygame.time.Clock()
running = True

#Constantes
DEFAULT_COLOR = (0,255,0)
COMMAND_TIMEOUT = 750
REPEAT_DELAY = 30 #milisseconds between each KEYDOWN event (when repeating)
KEY_TIMEOUT = 185 #MAX milisseconds between key pressings

screen_surface = pygame.display.set_mode((800,600))

command_timeout = -1
color = DEFAULT_COLOR
key_queue = []
key_timeout = -1
sprinting = False
pending_sprints = 0

pygame.key.set_repeat(REPEAT_DELAY*3, REPEAT_DELAY)
while running:
    clock.tick(30)
    pygame.draw.circle(screen_surface, color, (400,300) , 30)
    pygame.display.flip()
    if command_timeout >= 0:
        if (pygame.time.get_ticks() - command_timeout) > COMMAND_TIMEOUT:
            color = DEFAULT_COLOR
            command_timeout = -1

    if key_timeout >= 0:
        if (pygame.time.get_ticks() - key_timeout) > KEY_TIMEOUT:
            actual_state = 0
            key_timeout = -1

    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            running = False
        elif e.type == KEYDOWN:
            key_timeout = pygame.time.get_ticks()
            refresh_state(e.key)

