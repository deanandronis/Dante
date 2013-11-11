'''
Created on 31/10/2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, os, sys, Entities, functions, Constants, Globals

def level_1():
    floor_platform = Entities.Platform(32,16*32,30,1)
    wall_platform = Entities.Platform(0,0, 1, 17)
    wall_platform1 = Entities.Platform(32*30,0,1,17)
    end_block = Entities.goal_piece(28*32, 15*32)
    death_block = Entities.damage_tile(5*32,15*32)
    Globals.player = Entities.Player(32,32*14)
    Globals.hud = Entities.hud()

def level_2():
    floor_platform = Entities.Platform(32,16*32,30,1)
    wall_platform = Entities.Platform(0,0, 1, 17)
    wall_platform1 = Entities.Platform(32*30,0,1,17)
    end_block = Entities.goal_piece(28*32, 15*32)
    Globals.player = Entities.Player(32,32*14)
    Globals.hud = Entities.hud()
