'''
Created on Oct 27, 2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, sys, os, math, datetime
from pygame.locals import *
import Entities, functions, stage_1, Constants

#definitions
def load_level(levellayout):
    damagearray = []
    collisionleftright = levellayout[0]
    collisionupdown = levellayout[1]
    collisionalldir = levellayout[2]
    for index, value in enumerate(levellayout[3]):
        if isinstance(levellayout[3][index], Entities.Player):
            player = levellayout[3][index]
    
    for item in collisionleftright: sprites.append(item)
    for item in collisionupdown: sprites.append(item)
    for item in collisionalldir: sprites.append(item)
    hud = Entities.hud(1)
    damagearray.append(hud)
    return (player, hud, collisionleftright, collisionupdown, collisionalldir, damagearray)
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
player = load_level(stage_1.level_1())[0]
sprites.append(player)
hud = load_level(stage_1.level_1())[1]
collisionleftright = load_level(stage_1.level_1())[2]
collisionupdown = load_level(stage_1.level_1())[3]
collisionalldir = load_level(stage_1.level_1())[4]
damagearray = load_level(stage_1.level_1())[5]

ticktimer = 0
camera = Entities.Camera()

while not done:
    #Get and check events:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.xvel = -5
            elif event.key == pygame.K_RIGHT:
                player.xvel = 5
            elif event.key == pygame.K_UP:
                if player.touching_ground == True:
                    player.yvel = -12
                    player.gravity = 40
            elif event.key == pygame.K_DOWN:
                pass
            elif event.key == pygame.K_ESCAPE: done = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if not player.xvel > 0:
                    player.xvel = 0
            elif event.key == pygame.K_RIGHT:
                if not player.xvel < 0:
                    player.xvel = 0
            elif event.key == pygame.K_DOWN:
                pass
        
    
    #Write FPS in caption
    current_fps = float(clock.get_fps())
    pygame.display.set_caption("Dante's Inferbo     FPS: %s" % (str(current_fps)))
    
    #Update the hud and camera
    camera.updatecamera(player)
    hud.update(player.health)
    
    #Draw elements to screen
    if ticktimer%6 == 0: 
        for item in sprites:
            if type(item) == Entities.Player: item.animate()
    screen.fill((0,0,0))
    for sprite in sprites:
        screen.blit(sprite.image, (sprite.pos[0] - camera.x, sprite.pos[1] - camera.y))
    screen.blit(hud.image, (hud.x, hud.y))
    player.update(collisionleftright, collisionupdown, collisionalldir, damagearray)
    ticktimer += 1
    pygame.display.flip()
    clock.tick(MAX_FPS)