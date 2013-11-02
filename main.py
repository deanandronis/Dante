'''
Created on Oct 27, 2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, sys, os, math, datetime
from pygame.locals import *
import Entities, functions, stage_1
from stage_1 import level_1


#Variable init
pygame.init()
WINDOW_WIDTH = 800 #25
WINDOW_HEIGHT = 640 #20
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
blocklist = stage_1.level_1()
collisionleftright = blocklist[0]
collisionupdown = blocklist[1]
collisionalldir = blocklist[2]
for item in collisionleftright: sprites.append(item)
for item in collisionupdown: sprites.append(item)
for item in collisionalldir: sprites.append(item)
ticktimer = 0
camera = Entities.Camera()

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
                if max.touching_ground == True:
                    max.yvel = -12
                    max.gravity = 40
            elif event.key == pygame.K_DOWN:
                pass
            elif event.key == pygame.K_ESCAPE: done = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if not max.xvel > 0:
                    max.xvel = 0
            elif event.key == pygame.K_RIGHT:
                if not max.xvel < 0:
                    max.xvel = 0
            elif event.key == pygame.K_DOWN:
                pass
        
    
    #Write FPS in caption
    current_fps = float(clock.get_fps())
    pygame.display.set_caption("Dante's Inferbo     FPS: %s" % (str(current_fps)))
    
    #Draw elements to screen
    camera.updatecamera(max)
    if ticktimer%6 == 0: 
        for item in sprites:
            if type(item) == Entities.Player: item.animate()
    screen.fill((0,0,0))
    for sprite in sprites:
        screen.blit(sprite.image, (sprite.pos[0] - camera.x, sprite.pos[1] - camera.y))
    max.update(collisionleftright, collisionupdown, collisionalldir)
    ticktimer += 1
    pygame.display.flip()
    clock.tick(MAX_FPS)