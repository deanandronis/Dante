'''
Created on Nov 4, 2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, sys, os, Entities

pygame.init()

#initial variables
damagearray = []
collisionleftright = []
collisionupdown = []
collisionalldir = []
sprites = []
stage = 1
level = 1
player = None
hud= None



def reset_all(): #reset all variables back to starting values
    global damagearray
    global collisionleftright 
    global collisionupdown
    global collisionalldir   
    global sprites 
    global stage 
    global level
    damagearray = []
    collisionleftright = []
    collisionupdown = []
    collisionalldir = []
    sprites = []
    stage = 1
    level = 1


