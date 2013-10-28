'''
Created on Oct 27, 2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, sys, os, math, datetime
from pygame.locals import *
import Entities, functions


#Variable init
pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 680
WINDOW_SIZE = (WINDOW_WIDTH,WINDOW_HEIGHT)
BLOCK_SIZE = (BLOCK_WIDTH,BLOCK_HEIGHT) = 32,32
MAX_FPS = 60
sprites = []
done = False
global screen, clock
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
max = Entities.Player(400,340)
sprites.append(max)


while not done:
    #Get and check events:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                max.xvel = -5
            elif event.key == pygame.K_RIGHT:
                max.xvel = 5
            elif event.key == pygame.K_UP:
                pass
            elif event.key == pygame.K_DOWN:
                pass
            elif event.key == pygame.K_ESCAPE: done = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                max.xvel = 0
            elif event.key == pygame.K_RIGHT:
                max.xvel = 0
            elif event.key == pygame.K_UP:
                pass
            elif event.key == pygame.K_DOWN:
                pass
        
    
    #Write FPS in caption
    current_fps = float(clock.get_fps())
    pygame.display.set_caption("Dante's Inferbo     FPS: %s" % (str(current_fps)))
    
    #Draw elements to screen
    screen.fill((0,0,0))
    for sprite in sprites:
        screen.blit(sprite.image, sprite.pos)
    max.update()
    pygame.display.flip()
    clock.tick(MAX_FPS)