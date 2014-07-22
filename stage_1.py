'''
Created on 31/10/2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, os, sys, Entities, functions, Constants, Globals

def main_menu():
    pass

def level_trial():
    #render floors
    floor_1 = Entities.Platform(4*32, 22*32, 6, 4)
    floor_2 = Entities.Platform(15*32, 22*32,6, 4)
    floor_3 = Entities.Platform(24*32, 22*32, 10, 4)
    floor_4 = Entities.Platform(38*32,22*32, 8, 4)
    floor_5 = Entities.Platform(54*32,22*32, 4, 4)
    
    plat_1 = Entities.Platform(49*32,20*32, 1, 1)
    plat_3 = Entities.Platform(60*32,18*32, 1, 1)
    plat_5 = Entities.Platform(66*32,15*32, 1, 1)

        
    
    #render thingses
    troll = Entities.Troll(29*32,20*32, True, (24*32, 34*32), (24*32, 13*32, 10*32, 7*32))
    goalpiece = Entities.goal_piece(67*32, 13*32)
    trigger1 = Entities.event_trigger((18*32,0*32), (32, 22*32))
    trigger2 = Entities.event_trigger((40*32,0*32), (32, 22*32))
    trigger2 = Entities.event_trigger((56*32,0*32), (32, 22*32))

    
    #other stuff
    Globals.player = Entities.Player(6*32,20*32)
    Globals.hud = Entities.hud()
    Globals.camera.xbounds = (0, 70*32)
    Globals.camera.ybounds = (0, 960)
    Globals.camera.y = 420
    killborder = Entities.kill_border((0,Globals.camera.ybounds[1]), (70*32,128))
    narrator = Entities.Level_1_Narrator()
    Globals.event_manager = Entities.event_manager()
    Globals.event_manager.trigger_event()
    
    
    bg = Entities.Background(functions.get_image(os.path.join('Resources','Stage 1 Resources','BackgroundStage1.bmp'), (255,0,255)), 2240, 960)


def level_1():
    #render floors
    floor_1 = Entities.Platform(4*32, 22*32, 29, 4)
    floor_2 = Entities.Platform(37*32, 22*32, 11, 4)
    floor_3 = Entities.Platform(53*32, 22*32, 5, 4)
    floor_4 = Entities.Platform(61*32,22*32, 2, 4)
    
    #render thingses
    troll = Entities.Troll(38*32,20*32, True, (37*32, 48*32), (37*32, 22*32 - 64, 11*32, 2*32))
    wiki = Entities.Wikipedia(55*32 + 16, 17*32, 3*32)
    goalpiece = Entities.goal_piece(61*32 + 16, 21*32)
    
    #other stuff
    Globals.player = Entities.Player(6*32,20*32)
    Globals.hud = Entities.hud()
    Globals.camera.xbounds = (0, 70*32)
    Globals.camera.ybounds = (0, 960)
    Globals.camera.y = 420
    killborder = Entities.kill_border((0,Globals.camera.ybounds[1]), (70*32,128))
    narrator = Entities.Level_1_Narrator()
    Globals.event_manager = Entities.event_manager()
    Globals.event_manager.trigger_event()
    
    
    bg = Entities.Background(functions.get_image(os.path.join('Resources','Stage 1 Resources','BackgroundStage1.bmp'), (255,0,255)), 2240, 960)
    
def level_2():
    
    
    
    Globals.player = Entities.Player(32,32*14)
    Globals.hud = Entities.hud()
    
def boss_1():
    floor_platform = Entities.Platform(0*32, 12*32, 25, 5)
    Globals.player = Entities.Player(32*4,32*10)
    Globals.hud = Entities.hud()
    Globals.camera.xbounds = (0, 800)
    Globals.camera.ybounds = (0, 640)
    boss= Entities.InternetBoss(16*32, 6*32)