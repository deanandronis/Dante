'''
Created on 31/10/2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, os, sys, Entities, functions, Constants, Globals

def main_menu():
    pass

def level_1():
    #render floors
    floor_1 = Entities.Platform(4*32, 22*32, 29, 4)
    floor_2 = Entities.Platform(37*32, 22*32, 11, 4)
    floor_3 = Entities.Platform(53*32, 22*32, 5, 4)
    floor_4 = Entities.Platform(61*32,22*32, 1, 4)
    
    
    #other stuff
    Globals.player = Entities.Player(4*32,20*32)
    Globals.hud = Entities.hud()
    Globals.camera.xbounds = (0, 70*32)
    Globals.camera.ybounds = (0, 960)
    killborder = Entities.kill_border((0,Globals.camera.ybounds[1]), (70*32,128))
    bg = Entities.Background(functions.get_image(os.path.join('Resources','Stage 1 Resources','BackgroundStage1.bmp'), (255,0,255)), 2240, 960)
    
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