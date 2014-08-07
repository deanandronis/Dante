'''
Created on Nov 4, 2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, sys, os, Entities

pygame.init()

#initial variables
stage = 1
level = 0
player = None
hud= None
camera = None
event_manager = None
score = 0
key_pause = False

movinglist = []

#create sprite groups
group_PLAYER = pygame.sprite.GroupSingle()
group_COLLIDEBLOCKS = pygame.sprite.LayeredUpdates()
group_SPECIAL = pygame.sprite.LayeredUpdates()
group_PROJECTILES = pygame.sprite.Group()
group_AI = pygame.sprite.Group()
group_DRAWONLY = pygame.sprite.Group()
group_BG = pygame.sprite.Group()
group_BUTTON = pygame.sprite.Group()
group_BACKTILES = pygame.sprite.Group()
group_FILLBACKTILES = pygame.sprite.Group()
group_FRONTTILES = pygame.sprite.LayeredUpdates()

group_HUD = pygame.sprite.Group()
group_EVENTS = pygame.sprite.Group()
group_NARRATOR = pygame.sprite.Group()

def reset_all(): #reset all variables back to starting values
    global group_SPECIAL 
    global group_COLLIDEBLOCKS   
    global group_PLAYER
    global group_PROJECTILES
    global group_AI
    global stage 
    global level
    group_SPECIAL.empty()
    group_COLLIDEBLOCKS.empty()
    group_PLAYER.empty()
    group_PROJECTILES.empty()
    group_AI.empty()

    stage = 1
    level = 1

def clear_groups():
    global group_SPECIAL 
    global group_COLLIDEBLOCKS   
    global group_PLAYER
    global group_PROJECTILES
    global group_AI
    global group_DRAWONLY
    global group_BG
    global group_BUTTON
    global group_BACKTILES
    global group_EVENTS
    global group_NARRATOR
    global group_FRONTTILES
    global movinglist
    group_COLLIDEBLOCKS.empty()
    group_PLAYER.empty()
    group_SPECIAL.empty()
    group_PROJECTILES.empty()
    group_AI.empty()
    group_DRAWONLY.empty()
    group_BG.empty()
    group_BUTTON.empty()
    group_BACKTILES.empty()
    group_EVENTS.empty()
    group_NARRATOR.empty()
    group_FRONTTILES.empty()
    movinglist = []
    
def reset_variables():
    global player
    global hud
    global event_manager 
    global key_pause 
    player = None
    hud = None
    event_manager = None
    key_pause = False
    
    
    