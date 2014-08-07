'''
Created on Oct 27, 2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, sys, os, math, datetime
from pygame.locals import *
import Entities, functions, stage_1, Constants, Globals
from random import randrange
from Entities import Camera

#definitions
def next_level():
    Globals.level += 1
    if Globals.stage == 1:
        if Globals.level == 1:
            Globals.clear_groups()
            Globals.reset_variables()
            stage_1.level_1()





#Variable init
pygame.init() #initialise pygame modules
WINDOW_WIDTH = 768 #variable to store the width of the window
WINDOW_HEIGHT = 576 #HUD takes up bottom 3 #variable to store the height of the window
WINDOW_SIZE = (WINDOW_WIDTH,WINDOW_HEIGHT) #window size
BLOCK_SIZE = (BLOCK_WIDTH,BLOCK_HEIGHT) = 32,32 #size of the tiles in the game
MAX_FPS = 60 #the max FPS the game will run at
done = False #necessary for while loop
global screen, clock #variables for the screen and game timer
screen = pygame.display.set_mode(WINDOW_SIZE) #creates the window
clock = pygame.time.Clock() #creates a controller for the game cycles
ticktimer = 0 #variable to calculate the time that has passed
mousex, mousey = (0,0)
Globals.camera = Entities.Camera() #create the camera
stage_1.level_4() #load level 1

while not done:
    keypressed = pygame.key.get_pressed()
    #test next level
    if Globals.player.next_level == True:
        Globals.player.next_level = False
        next_level()

    #Get and check events:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True #exit the game if player presses cross button
        elif event.type == pygame.KEYDOWN and not Globals.key_pause:
            if event.key == pygame.K_UP:#up arrow key pressed
                if Globals.player.arrowkey_enabled:
                    if Globals.player.touching_ground: #check to see if player is touching ground
                        Globals.player.yvel = -10 #accelerate the player upwards
                        Globals.player.y -= 4
            elif event.key == pygame.K_DOWN:
                Globals.player.health -= 1
                Globals.event_manager.throw_chat()

            elif event.key == pygame.K_z:
                if Globals.player.can_attack:
                    Globals.player.attack = 'slash'
                    Globals.player.attacking = True
                    Globals.player.can_attack = False
                    Globals.player.sprinting = False
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
                        #cheat keys        
            elif event.key == pygame.K_t:
                if Globals.player.can_attack:
                    Globals.player.attack = 'teabag'
                    Globals.player.attacking = True
                    Globals.player.arrowkey_enabled = False
                    Globals.player.can_attack = False
                    Globals.player.xvel = 0
                elif Globals.player.can_attack == False and Globals.player.attack == 'teabag':
                    Globals.player.attacking = False
                    Globals.player.arrowkey_enabled = True
                    Globals.player.can_attack = True
            
            elif event.key == pygame.K_RETURN: 
                for item in Globals.group_EVENTS:
                    if item.waiting_for_proceed == True: 
                        item.waiting_for_proceed = False
                        
                        item.next_event()
            elif event.key == pygame.K_HOME: Globals.player.yvel = -12
            elif event.key == pygame.K_ESCAPE: done = True #exit the game if player presses escape
            elif event.key == pygame.K_F1: block = Entities.damage_tile(pygame.mouse.get_pos()[0] + Globals.camera.x, pygame.mouse.get_pos()[1] + Globals.camera.y)
            elif event.key == pygame.K_F12: coin = Entities.Coin(pygame.mouse.get_pos()[0] + Globals.camera.x, pygame.mouse.get_pos()[1] + Globals.camera.y)
            elif event.key == pygame.K_F11: 
                Globals.player.yvel = 0
                if Globals.player.gravity: Globals.player.gravity = False
                else: Globals.player.gravity = True
        elif event.type == MOUSEBUTTONDOWN: 
            mousex, mousey = event.pos
            print "Mouse: " + str((mousex + Globals.camera.x, mousey + Globals.camera.y))
           
    #movement
    if keypressed[K_LEFT] and not Globals.player.keys['right'] == True:
                Globals.player.left_pressed()     
                Globals.player.keys['left'] = True
                
    elif not keypressed[K_LEFT] and Globals.player.keys['left'] == True:
            Globals.player.left_released()                
            Globals.player.keys['left'] = False
            
    if keypressed[K_RIGHT] and Globals.player.keys['left'] == False:
            Globals.player.right_pressed()
            Globals.player.keys['right'] = True
            
    elif not keypressed[K_RIGHT] and Globals.player.keys['right'] == True:     
        Globals.player.right_released()
        Globals.player.keys['right'] = False
    
    if not keypressed[K_RIGHT] and not keypressed[K_LEFT]:
        if Globals.player.keys['left']: 
            Globals.player.left_released()
        if Globals.player.keys['right']: 
            Globals.player.right_released()        
    
    #Write FPS in caption
    current_fps = float(clock.get_fps()) #get the current FPS
    pygame.display.set_caption("Dante's Inferbo     FPS: %s" % (str(current_fps))) #set the window caption 
    for item in Globals.movinglist: item.move()

    if ticktimer%Globals.player.animatetimer == 0 and not Globals.key_pause: 

        for item in Globals.group_PLAYER: #animate the player every 6 cycles
            item.animate()
    if not Globals.key_pause:
        Globals.player.update() #update the player
        Globals.group_PROJECTILES.update()

    #Update the hud and Globals.camera
    Globals.camera.updatecamera(Globals.player) #update the Globals.camera's position to centre window on player
    Globals.hud.update(Globals.player.health) #redraw the hud elements
    
    
    #Draw elements to screen       
    screen.fill((0,0,0)) #wipe the screen
    
    for item in Globals.group_BG:
        if item.move_with_camera:
            screen.blit(item.image, (item.pos[0] - Globals.camera.x, item.pos[1] - Globals.camera.y)) #account for Globals.camera location
        else: 
            screen.blit(item.image, (item.pos)) #account for Globals.camera location
            
    for item in Globals.group_BACKSPECIAL: #draw the projectiles to screen
        item.update()
        if item.rect.x < Globals.camera.x + Globals.camera.width or item.rect.x + item.rect.width > Globals.camera.x:
            screen.blit(item.image, (item.rect.x - Globals.camera.x, item.rect.y - Globals.camera.y)) #account for Globals.camera location

            
    for item in Globals.group_BACKTILES: #draw the wall and floor objects to screen
        if item.pos[0] < Globals.camera.x + Globals.camera.width or item.pos[0] + item.image.get_width() > Globals.camera.x:
            screen.blit(item.image, (item.pos[0] - Globals.camera.x, item.pos[1] - Globals.camera.y)) #account for Globals.camera location

    for item in Globals.group_FILLBACKTILES: #draw the wall and floor objects to screen
        if item.pos[0] < Globals.camera.x + Globals.camera.width or item.pos[0] + item.image.get_width() > Globals.camera.x:
            screen.blit(item.image, (item.pos[0] - Globals.camera.x, item.pos[1] - Globals.camera.y)) #account for Globals.camera location



    for item in Globals.group_PLAYER: #draw the wall and floor objects to screen
        screen.blit(item.image, (item.x - Globals.camera.x, item.y - Globals.camera.y)) #account for Globals.camera location
    
    for item in Globals.group_COLLIDEBLOCKS: #draw the wall and floor objects to screen
        if item.rect.x < Globals.camera.x + Globals.camera.width or item.rect.x + item.rect.width > Globals.camera.x:
            screen.blit(item.image, (item.pos[0] - Globals.camera.x, item.pos[1] - Globals.camera.y)) #account for Globals.camera location

    for item in Globals.group_FRONTTILES: #draw the wall and floor objects to screen
        if item.pos[0] < Globals.camera.x + Globals.camera.width or item.pos[0] + item.image.get_width() > Globals.camera.x:
            screen.blit(item.image, (item.pos[0] - Globals.camera.x, item.pos[1] - Globals.camera.y)) #account for Globals.camera location


    for item in Globals.group_AI:
        if not Globals.key_pause:
            item.update()
            if ticktimer%6==0: item.animate()
        if item.x < Globals.camera.x + Globals.camera.width or item.rect.x + item.rect.width > Globals.camera.x:
            screen.blit(item.image, (item.rect.x - Globals.camera.x, item.rect.y - Globals.camera.y))
        
    for item in Globals.group_SPECIAL:
        if not Globals.key_pause:
            if isinstance(item, Entities.movingtext): item.update()
        if isinstance(item, Entities.key): item.update()
        if isinstance(item, Entities.passable_top): item.collide()
        if isinstance(item, Entities.event_trigger): pass
        elif item.rect.x < Globals.camera.x + Globals.camera.width or item.rect.x + item.rect.width > Globals.camera.x:
            if isinstance(item, Entities.kill_border): pass
            elif isinstance(item, Entities.spike_box): screen.blit(item.image, (item.pos[0]- Globals.camera.x, item.pos[1] - Globals.camera.y))
            else: screen.blit(item.image, (item.rect.x - Globals.camera.x, item.rect.y - Globals.camera.y)) #draw whatever else is in the group
    
    for item in Globals.group_PROJECTILES: #draw the projectiles to screen
        if ((isinstance(item, Entities.Television) or isinstance(item, Entities.shoutProj)) or isinstance(item, Entities.WikiProj) and ticktimer%6==0) and not Globals.key_pause: item.animate()
        if item.rect.x < Globals.camera.x + Globals.camera.width or item.rect.x + item.rect.width > Globals.camera.x:
            screen.blit(item.image, (item.rect.x - Globals.camera.x, item.rect.y - Globals.camera.y)) #account for Globals.camera location
    
    for item in Globals.group_HUD:
        screen.blit(item.image, (0, 576-96)) #draw the HUD to the screen
        
    for item in Globals.group_NARRATOR:
        if isinstance(item, Entities.Narrator): screen.blit(item.image, (630,447))
        elif isinstance(item, Entities.text_bubble): 
            screen.blit(item.image, (item.rect.x, item.rect.y))
            if isinstance(item, Entities.text_bubble_right_narrator_timed): 
                item.update()
    
    for item in Globals.group_BUTTON:
        screen.blit(item.image, item.pos)
        if item.rect.collidepoint((mousex, mousey)): 
            (mousex, mousey) = (0,0)
            item.clicked()

    for item in Globals.group_DRAWONLY: screen.blit(item.image, (item.rect.x - Globals.camera.x, item.rect.y - Globals.camera.y))
    ticktimer += 1 #add one to the number of cycles
    pygame.display.flip() #refresh the screen
    clock.tick(MAX_FPS) #limit number of game cycles to 60