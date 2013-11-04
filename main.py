'''
Created on Oct 27, 2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, sys, os, math, datetime
from pygame.locals import *
import Entities, functions, stage_1, Constants, Globals
from Globals import damagearray

#definitions
def load_level(levellayout):
    Globals.collisionleftright = levellayout[0]
    Globals.collisionupdown = levellayout[1]
    Globals.collisionalldir = levellayout[2]
    for index, value in enumerate(levellayout[3]):
        if isinstance(levellayout[3][index], Entities.Player):
            Globals.player = levellayout[3][index]
            Globals.sprites.append(Globals.player)
    Globals.damagearray = levellayout[4]
    for item in Globals.collisionleftright: Globals.sprites.append(item)
    for item in Globals.collisionupdown: Globals.sprites.append(item)
    for item in Globals.collisionalldir: Globals.sprites.append(item)
    for item in Globals.damagearray: Globals.sprites.append(item)
    Globals.hud = Entities.hud(levellayout[5])
    
    


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
        pass
    
    #test blocks to be destroyed
    from test.test_iterlen import len
    if not len(Globals.player.destroyblock) == 0:
        for item in Globals.player.destroyblock:
            pass
    
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
        for item in Globals.sprites:
            if type(item) == Entities.Player: item.animate()
    screen.fill((0,0,0))
    for sprite in Globals.sprites:
        screen.blit(sprite.image, (sprite.pos[0] - camera.x, sprite.pos[1] - camera.y))
   
    screen.blit(Globals.hud.image, (Globals.hud.x, Globals.hud.y))
    Globals.player.update(Globals.collisionleftright, Globals.collisionupdown, Globals.collisionalldir, Globals.damagearray)
    ticktimer += 1
    pygame.display.flip()
    clock.tick(MAX_FPS)