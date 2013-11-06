'''
Created on Oct 27, 2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, sys, os, math, datetime
from pygame.locals import *
import Entities, functions, stage_1, Constants, Globals

#definitions
def load_level():
    floor_platform = Entities.Platform(32,16*32,30,1)
    wall_platform = Entities.Platform(0,0, 1, 17)
    wall_platform1 = Entities.Platform(32*30,0,1,17)
    Globals.player = Entities.Player(32,32)
    Globals.hud = Entities.hud(1)


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
load_level() #load level 1

ticktimer = 0 #variable to calculate the time that has passed
camera = Entities.Camera() #create the camera

while not done:
    #test next level
    if Globals.player.next_level == True:
        Globals.player.next_level = False
        

    #Get and check events:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True #exit the game if player presses cross button
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Globals.player.xvel = -5 #left arrow key down; set player's horizontal velocity to -5 (5 units/cycle left)
            elif event.key == pygame.K_RIGHT:
                Globals.player.xvel = 5 #right arrow key pressed; set player's horizontal velocity to 5 (5 units/cycle right)
            elif event.key == pygame.K_UP:#up arrow key pressed
                if Globals.player.touching_ground: #check to see if player is touching ground
                    Globals.player.yvel = -12 #accelerate the player upwards
            elif event.key == pygame.K_DOWN:
                pass
            elif event.key == pygame.K_ESCAPE: done = True #exit the game if player presses escape
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: #left key released
                if not Globals.player.xvel > 0: #set the player's horizontal velocity to 0 if player isn't moving right
                    Globals.player.xvel = 0 
            elif event.key == pygame.K_RIGHT: #right key released
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
    
    #Update the hud and camera
    camera.updatecamera(Globals.player) #update the camera's position to centre window on player
    Globals.hud.update(Globals.player.health) #redraw the hud elements
    
    
    
    #Draw elements to screen       
    screen.fill((0,0,0)) #wipe the screen
    for item in Globals.group_COLLIDEBLOCKS: #draw the wall and floor objects to screen
        screen.blit(item.image, (item.pos[0] - camera.x, item.pos[1] - camera.y)) #account for camera location
        
    for item in Globals.group_PLAYER: #draw the wall and floor objects to screen
        screen.blit(item.image, (item.rect.x - camera.x, item.rect.y - camera.y)) #account for camera location
        
    Globals.group_SPECIAL.draw(screen) #draw the HUD to the screen
    
    ticktimer += 1 #add one to the number of cycles
    pygame.display.flip() #refresh the screen
    clock.tick(MAX_FPS) #limit number of game cycles to 60