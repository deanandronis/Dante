'''
Created on Oct 27, 2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, sys, os, math, datetime
from pygame.locals import *
import Entities, functions, stage_1, Constants, Globals
from random import randrange


#definitions
def next_level():
    if Globals.stage == 1:
        if Globals.level == 1:
            Globals.clear_groups()
            stage_1.level_2()

#Variable init
pygame.init() #initialise pygame modules
WINDOW_WIDTH = 800 #25 blocks #variable to store the width of the window
WINDOW_HEIGHT = 640 #20 blocks; HUD takes up bottom 3 #variable to store the height of the window
WINDOW_SIZE = (WINDOW_WIDTH,WINDOW_HEIGHT) #window size
BLOCK_SIZE = (BLOCK_WIDTH,BLOCK_HEIGHT) = 32,32 #size of the tiles in the game
MAX_FPS = 60 #the max FPS the game will run at
done = False #necessary for while loop
global screen, clock #variables for the screen and game timer
screen = pygame.display.set_mode(WINDOW_SIZE) #creates the window
clock = pygame.time.Clock() #creates a controller for the game cycles
ticktimer = 0 #variable to calculate the time that has passed
Globals.camera = Entities.Camera() #create the camera
stage_1.level_1() #load level 1



while not done:
    #test next level
    if Globals.player.next_level == True:
        Globals.player.next_level = False
        next_level()

    #Get and check events:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True #exit the game if player presses cross button
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if Globals.player.arrowkey_enabled:
                    Globals.player.xvel = -5 #left arrow key down; set player's horizontal velocity to -5 (5 units/cycle left)
            elif event.key == pygame.K_RIGHT:
                if Globals.player.arrowkey_enabled:
                    Globals.player.xvel = 5 #right arrow key pressed; set player's horizontal velocity to 5 (5 units/cycle right)
            elif event.key == pygame.K_UP:#up arrow key pressed
                if Globals.player.arrowkey_enabled:
                    if Globals.player.touching_ground: #check to see if player is touching ground
                        Globals.player.yvel = -12 #accelerate the player upwards
            elif event.key == pygame.K_DOWN:
                Globals.player.health -= 1
            elif event.key == pygame.K_z:
                if Globals.player.can_attack:
                    Globals.player.attack = 'slash'
                    Globals.player.attacking = True
                    Globals.player.can_attack = False
            elif event.key == pygame.K_x: #x key pressed - spin
                if Globals.player.can_attack:
                    Globals.player.attack = 'spin'
                    Globals.player.attacking = True
                    Globals.player.arrowkey_enabled = False
                    Globals.player.can_attack = False
                    Globals.player.xvel = 0
            elif event.key == pygame.K_c:
                if Globals.player.can_attack:
                    Globals.player.attack = 'shout'
                    Globals.player.attacking = True
                    Globals.player.arrowkey_enabled = False
                    Globals.player.can_attack = False
                    Globals.player.xvel = 0
            elif event.key == pygame.K_v:
                if Globals.player.can_attack:
                    Globals.player.attack = 'lazer'
                    Globals.player.attacking = True
                    Globals.player.arrowkey_enabled = False
                    Globals.player.can_attack = False
                    Globals.player.xvel = 0
            elif event.key == pygame.K_ESCAPE: done = True #exit the game if player presses escape
            elif event.key == pygame.K_F1: block = Entities.damage_tile(pygame.mouse.get_pos()[0] + Globals.camera.x, pygame.mouse.get_pos()[1] + Globals.camera.y)
            elif event.key == pygame.K_F2: troll = Entities.Troll(pygame.mouse.get_pos()[0] + Globals.camera.x, pygame.mouse.get_pos()[1] + Globals.camera.y, False)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: #left key released
                if not Globals.player.xvel > 0 and Globals.player.arrowkey_enabled: #set the player's horizontal velocity to 0 if player isn't moving right
                    Globals.player.xvel = 0 
            elif event.key == pygame.K_RIGHT and Globals.player.arrowkey_enabled: #right key released
                if not Globals.player.xvel < 0: #set the player's horizontal velocity to 0 if player isn't moving left
                    Globals.player.xvel = 0
            elif event.key == pygame.K_DOWN:
                pass
        
    
    #Write FPS in caption
    current_fps = float(clock.get_fps()) #get the current FPS
    pygame.display.set_caption("Dante's Inferbo     FPS: %s" % (str(current_fps))) #set the window caption 
    
    if ticktimer%6 == 0: 
        for item in Globals.group_PLAYER: #animate the player every 6 cycles
            item.animate()
    Globals.player.update() #update the player
    Globals.group_PROJECTILES.update()
    #Update the hud and Globals.camera
    Globals.camera.updatecamera(Globals.player) #update the Globals.camera's position to centre window on player
    Globals.hud.update(Globals.player.health) #redraw the hud elements
    
    #Draw elements to screen       
    screen.fill((0,0,0)) #wipe the screen
    for item in Globals.group_COLLIDEBLOCKS: #draw the wall and floor objects to screen
        screen.blit(item.image, (item.pos[0] - Globals.camera.x, item.pos[1] - Globals.camera.y)) #account for Globals.camera location
        
    
    for item in Globals.group_PROJECTILES: #draw the projectiles to screen
        if (isinstance(item, Entities.Television) or isinstance(item, Entities.shoutProj)) and ticktimer%6==0: item.animate()
        screen.blit(item.image, (item.rect.x - Globals.camera.x, item.rect.y - Globals.camera.y)) #account for Globals.camera location
    for item in Globals.group_PLAYER: #draw the wall and floor objects to screen
        screen.blit(item.image, (item.rect.x - Globals.camera.x, item.rect.y - Globals.camera.y)) #account for Globals.camera location
    for item in Globals.group_AI:
        item.update()
        if ticktimer%6==0: item.animate()
#         pygame.draw.line(screen,(255,255,255), (item.rect.x + item.rect.width/2 - Globals.camera.x, item.rect.y + item.rect.height/2 - Globals.camera.y), (Globals.player.rect.x + Globals.player.rect.width/2 - Globals.camera.x, Globals.player.rect.y + Globals.player.rect.height/2 - Globals.camera.y))
        screen.blit(item.image, (item.rect.x - Globals.camera.x, item.rect.y - Globals.camera.y))
    for item in Globals.group_SPECIAL:
        if isinstance(item, Entities.movingtext): item.update()
        if isinstance(item, Entities.hud):
            screen.blit(item.image, item.rect) #draw the HUD to the screen
        else:
            screen.blit(item.image, (item.rect.x - Globals.camera.x, item.rect.y - Globals.camera.y)) #draw whatever else is in the group

    ticktimer += 1 #add one to the number of cycles
    pygame.display.flip() #refresh the screen
    clock.tick(MAX_FPS) #limit number of game cycles to 60