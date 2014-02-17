'''
Created on 31/10/2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, os, sys, Entities, functions, Constants, Globals

def main_menu():
    pass

def level_1():
    #render floors
    floor_1 = Entities.Platform(4*32,12*32, 52,5)
    floor_2 = Entities.Platform(63*32, 12*32, 5, 5)
    floor_3 = Entities.Platform(75*32, 12*32, 27, 5)
    floor_4 = Entities.Platform(20*32, 10*32, 15, 1)
    Floor_5 = Entities.Platform(40*32, 7*32, 10, 1)
    
    #render enemies, coins etc
        #coins
    for i in range(1,4):
        coin = Entities.Coin(48*32, (i+3)*32)
        coin = Entities.Coin(49*32, (i+3)*32) 
    coin = Entities.Coin(43*32, 9*32)
    coin = Entities.Coin(46*32, 9*32)
    coin = Entities.Coin(49*32, 9*32)
    
        #enemies
    wiki = Entities.Wikipedia(44*32, 3*32, 2*32)
    troll = Entities.Troll(27*32,8*32, True, floor_4)
        #specials
    goalpiece = Entities.goal_piece(101*32,10*32)    
    
    #other stuff
    Globals.player = Entities.Player(10*32,32*10)
    Globals.hud = Entities.hud()
    Globals.camera.xbounds = (0, 106*32)
    Globals.camera.ybounds = (0, 640)
    
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