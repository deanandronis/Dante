'''
Created on Oct 27, 2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, sys, os, math, datetime
from pygame.locals import *
import Entities, functions, stage_1, Constants, Globals

#definitions
def load_level():
    floor_platform = Entities.Platform(32,400,10,1)
    wall_platform = Entities.Platform(300,200, 1, 9)
    wall_platform1 = Entities.Platform(32,200,1,9)
    Globals.player = Entities.Player(32,32)
    Globals.hud = Entities.hud(1)


#Variable init
pygame.init()
WINDOW_WIDTH = 800 #25
WINDOW_HEIGHT = 640 #20
WINDOW_SIZE = (WINDOW_WIDTH,WINDOW_HEIGHT)
BLOCK_SIZE = (BLOCK_WIDTH,BLOCK_HEIGHT) = 32,32
MAX_FPS = 60
done = False
global screen, clock
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
load_level()

ticktimer = 0
camera = Entities.Camera()

while not done:
    #test next level
    if Globals.player.next_level == True:
        Globals.player.next_level = False
        

    #Get and check events:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Globals.player.xvel = -5
            elif event.key == pygame.K_RIGHT:
                Globals.player.xvel = 5
            elif event.key == pygame.K_UP:
                if Globals.player.touching_ground == True:
                    Globals.player.yvel = -12
                    Globals.player.gravity = 40
            elif event.key == pygame.K_DOWN:
                pass
            elif event.key == pygame.K_ESCAPE: done = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if not Globals.player.xvel > 0:
                    Globals.player.xvel = 0
            elif event.key == pygame.K_RIGHT:
                if not Globals.player.xvel < 0:
                    Globals.player.xvel = 0
            elif event.key == pygame.K_DOWN:
                pass
        
    
    #Write FPS in caption
    current_fps = float(clock.get_fps())
    pygame.display.set_caption("Dante's Inferbo     FPS: %s" % (str(current_fps)))
    
    #Update the hud and camera
    camera.updatecamera(Globals.player)
    Globals.hud.update(Globals.player.health)
    
    #Draw elements to screen
    if ticktimer%6 == 0: 
        for item in Globals.group_PLAYER:
            item.animate()
    screen.fill((0,0,0))
    Globals.group_UDLR.draw(screen)
    Globals.group_PLAYER.draw(screen)
    for sprite in Globals.group_SPECIAL:
        screen.blit(sprite.image, (sprite.pos[0] - camera.x, sprite.pos[1] - camera.y))
    Globals.player.update()
    ticktimer += 1
    pygame.display.flip()
    clock.tick(MAX_FPS)