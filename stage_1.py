'''
Created on 31/10/2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, os, sys, Entities, functions, Constants, Globals

def level_1():
    floor_platform = Entities.Platform(4*32,12*32, 50,5)
    end_block = Entities.goal_piece(51*32, 11*32)
    death_block = Entities.damage_tile(14*32,11*32)
    Globals.player = Entities.Player(10*32,32*10)
    Globals.hud = Entities.hud()
    Globals.camera.xbounds = (0, 58*32)
    Globals.camera.ybounds = (0, 640)
    small_plat = Entities.Platform(10*32, 5*32, 10, 2)
    troll = Entities.Troll(15*32, 3*32 + 16, True, small_plat)
    wiki = Entities.Wikipedia(15*32, 8*32, 50)
    
def level_2():
    floor_platform = Entities.Platform(32,16*32,30,1)
    wall_platform = Entities.Platform(0,0, 1, 17)
    wall_platform1 = Entities.Platform(32*30,0,1,17)
    end_block = Entities.goal_piece(28*32, 15*32)
    coin_block = Entities.Coin(27*32, 15*32)
    Globals.player = Entities.Player(32,32*14)
    Globals.hud = Entities.hud()
    
def boss_1():
    floor_platform = Entities.Platform(0*32, 12*32, 25, 5)
    Globals.player = Entities.Player(32*4,32*10)
    Globals.hud = Entities.hud()
    Globals.camera.xbounds = (0, 800)
    Globals.camera.ybounds = (0, 640)
    boss= Entities.InternetBoss(16*32, 6*32)