import pygame
from pygame.locals import *
from sys import exit

                    #0  1  2  3  4  5  6  7  8  9  10 11 12 13
commands_automata= [[11,0, 0, 4, 0, 0, 0, 0, 0, 11,0, 0, 13,0],#up
                    [9, 2, 0, 0, 0, 0, 0, 0, 0, 10,0, 12,0, 0],#down
                    [0, 6, 3, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],#left
                    [1, 0, 0, 0, 5, 0, 7, 0, 0, 0, 0, 0, 0, 0]]#right
actual_state = 0

def refresh_state(in_key = -1):
    global actual_state
    global commands_automata

    input = -1
    if in_key == K_UP: input = 0
    elif in_key == K_DOWN: input = 1
    elif in_key == K_LEFT: input = 2
    elif in_key == K_RIGHT: input = 3
    actual_state = commands_automata[input][actual_state]

    if actual_state == 5: doRoll()
    if actual_state == 8: doSprint()
    if actual_state == 10: doGetDown()
    if actual_state == 11: doJump()
    if actual_state == 13: doClimb()

def doRoll():
    global color
    color = (0,0,255)
    global command_timeout
    command_timeout = pygame.time.get_ticks()

def doSprint():
    global color
    color = (255,0,255)
    global command_timeout
    command_timeout = pygame.time.get_ticks()

def doGetDown():
    global color
    color = (0,255,255)
    global command_timeout
    command_timeout = pygame.time.get_ticks()

def doJump():
    global color
    color = (255,255,0)
    global command_timeout
    command_timeout = pygame.time.get_ticks()

def doClimb():
    global color
    color = (255,255,255)
    global command_timeout
    command_timeout = pygame.time.get_ticks()

