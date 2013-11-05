'''
Created on Oct 27, 2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, sys, os, math, datetime
from pygame.locals import *
import Entities, functions, stage_1, Constants, Globals

#definitions
def load_level(levellayout):
    Globals.collisionleftright = levellayout[0]
    Globals.collisionupdown = levellayout[1]
    Globals.collisionalldir = levellayout[2]
    for item in levellayout[0]: Globals.group_LR.add(item)
    for item in levellayout[1]: Globals.group_UD.add(item)
    for item in levellayout[2]: Globals.group_UDLR.add(item)
    for index, value in enumerate(levellayout[3]):
        if isinstance(levellayout[3][index], Entities.Player):
            Globals.player = levellayout[3][index]
    Globals.hud = Entities.hud(levellayout[5])

    
    
def next_level():
    if Globals.stage == 1:
        if Globals.level == 1:
            Globals.level += 1
            Globals.clear_groups()
            load_level(stage_1.level_2())


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
load_level(stage_1.level_1())


ticktimer = 0
camera = Entities.Camera()

while not done:
    #test next level
    if Globals.player.next_level == True:
        Globals.player.next_level = False
        next_level()

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
    for sprite in Globals.group_PLAYER:
        screen.blit(sprite.image, (sprite.pos[0] - camera.x, sprite.pos[1] - camera.y))
    for sprite in Globals.group_LR:
        screen.blit(sprite.image, (sprite.pos[0] - camera.x, sprite.pos[1] - camera.y))
    for sprite in Globals.group_UD:
        screen.blit(sprite.image, (sprite.pos[0] - camera.x, sprite.pos[1] - camera.y))
        pass
    for sprite in Globals.group_UDLR:
        screen.blit(sprite.image, (sprite.pos[0] - camera.x, sprite.pos[1] - camera.y))
    for sprite in Globals.group_SPECIAL:
        screen.blit(sprite.image, (sprite.pos[0] - camera.x, sprite.pos[1] - camera.y))
    Globals.player.update()
    ticktimer += 1
    pygame.display.flip()
    clock.tick(MAX_FPS)