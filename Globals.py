'''
Created on Nov 4, 2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, sys, os, Entities

pygame.init()

#initial variables
stage = 1
level = 1
player = None
hud= None

#create sprite groups
group_PLAYER = pygame.sprite.Group()
group_COLLIDEBLOCKS = pygame.sprite.Group()
group_SPECIAL = pygame.sprite.Group()

def reset_all(): #reset all variables back to starting values
    global group_SPECIAL 
    global group_COLLIDEBLOCKS   
    global group_PLAYER
    global stage 
    global level
    group_LR.empty()
    group_SPECIAL.empty()
    group_UD.empty()
    group_COLLIDEBLOCKS.empty()
    group_PLAYER.empty()
    stage = 1
    level = 1

def clear_groups():
    global group_LR
    global group_SPECIAL 
    global group_UD
    global group_COLLIDEBLOCKS   
    global group_PLAYER
    group_LR.empty()
    group_SPECIAL.empty()
    group_UD.empty()
    group_COLLIDEBLOCKS.empty()
    group_PLAYER.empty()