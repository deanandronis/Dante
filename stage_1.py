'''
Created on 31/10/2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, os, sys, Entities, functions, Constants, Globals

def level_1():
    floor_platform = Entities.Platform(4*32,12*32, 50,5)
    end_block = Entities.goal_piece(51*32, 11*32)
    death_block = Entities.damage_tile(14*32,11*32)
    small_plat = Entities.Platform(2*32, 4*32, 10, 2)
    Globals.player = Entities.Player(6*32,32*10)
    Globals.hud = Entities.hud()
    troll = Entities.Troll(32*2,32*2 + 16, True, small_plat)
    Globals.camera.xbounds = (0, 58*32)
    Globals.camera.ybounds = (0, 640)
    
def level_2():
    floor_platform = Entities.Platform(32,16*32,30,1)
    wall_platform = Entities.Platform(0,0, 1, 17)
    wall_platform1 = Entities.Platform(32*30,0,1,17)
    end_block = Entities.goal_piece(28*32, 15*32)
    coin_block = Entities.Coin(27*32, 15*32)
    Globals.player = Entities.Player(32,32*14)
    Globals.hud = Entities.hud()
