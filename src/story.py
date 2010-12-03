import pygame
from pygame.locals import *
import sys, os

pygame.init()
running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Good Intentions")
story = []
for i in range(0,6):
    story.append(pygame.image.load(os.path.join('', 'stories/prologo01', '0' + str(i+1) + '.jpg' )))
print story

actual_image = story[0]

def next_image():
    global story
    global actual_image
    fill_surf = pygame.Surface((1024,768))
    fill_surf.fill((10,10,10))
    alpha = 0
    fill_surf.set_alpha(alpha)
    while alpha < 255:
        clock.tick(25)
        alpha+=35
        fill_surf.set_alpha(alpha)
        screen.blit(fill_surf, (0,0))
        pygame.display.flip()
    story.pop(0)
    actual_image = story[0]
    while alpha > 0:
        clock.tick(25)
        alpha-=35
        fill_surf.set_alpha(alpha)
        screen.blit(actual_image, (0,0))
        screen.blit(fill_surf, (0,0))
        pygame.display.flip()

adj_x, adj_y = 0 , 0
while running:
    clock.tick(25)
    screen.blit(actual_image, (0 - adj_x, 0 - adj_y))
    adj_x += 0.5
    adj_y += 0.5
    if actual_image.get_width() < screen.get_width() + adj_x or actual_image.get_height() < screen.get_height() + adj_y:
        adj_x = 0
        adj_y = 0
        next_image()
    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            running = False
    pygame.display.flip()
        
    
