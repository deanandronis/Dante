'''
Created on 31/10/2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, os, sys, Entities, functions, Constants, Globals

def main_menu():
    pass

def level_trial():
            
    move = Entities.moving(4*32, 16*32, 3*32*0, 3*32, 0, 1)        
    
    #render floors
    floor_1 = Entities.Platform(4*32, 22*32, 6, 4)
    floor_2 = Entities.Platform(14*32, 22*32,6, 4)
    floor_3 = Entities.Platform(24*32, 22*32, 10, 4)
    floor_4 = Entities.Platform(38*32,22*32, 8, 4)
    floor_5 = Entities.Platform(54*32,22*32, 4, 4)
    
    plat_1 = Entities.Platform(49*32,20*32, 1, 1)
    plat_3 = Entities.Platform(60*32,18*32, 1, 1)
    plat_5 = Entities.Platform(66*32,15*32, 1, 1)

  
    
    #render thingses
    troll = Entities.Troll(29*32,20*32, True, (24*32, 34*32), (24*32, 13*32, 10*32, 9*32))
    goalpiece = Entities.goal_piece(67*32, 13*32)
    trigger1 = Entities.event_trigger((18*32,0*32), (32, 22*32))
    trigger2 = Entities.event_trigger((40*32,0*32), (32, 22*32))
    trigger2 = Entities.event_trigger((56*32,0*32), (32, 22*32))

    for i in range(18,21):
        coin= Entities.Coin(42*32, i*32)
    
    #other stuff
    Globals.player = Entities.Player(6*32,20*32)
    Globals.hud = Entities.hud()
    Globals.camera.xbounds = (0, 70*32)
    Globals.camera.ybounds = (0, 960)
    Globals.camera.y = 420
    killborder = Entities.kill_border((0,Globals.camera.ybounds[1]), (70*32,128))
    narrator = Entities.Stage_1_Narrator()
    Globals.event_manager = Entities.event_manager()
    Globals.event_manager.trigger_event()
    
    
    bg = Entities.Background(functions.get_image(os.path.join('Resources','Stage 1 Resources','BackgroundStage1.bmp'), (255,0,255)), 2240, 960)


def level_1():  
    
    #test
    door_1 = Entities.Door(5*32, 9*32, 1, 1, 1)
    
    #render floors
    floor_1 = Entities.Platform(2*32, 7*56, 4, 5)
    floor_2 = Entities.Platform(9*32, 7*56, 4, 5)
    floor_3 = Entities.Platform(5*32, 8*56, 5, 4)
    
    floor_4 = Entities.Platform(16*32 + 0, 9*56, 6, 3)
    floor_5 = Entities.Platform(25*32, 8*56, 6, 4)
    floor_6 = Entities.Platform(12*32, 10*56, 5, 2)
    floor_7 = Entities.Platform(21*32, 10*56, 5, 2)

    floor_8 = Entities.Platform(31*32, 15*56, 6, 11)
    
    floor_9 = Entities.Platform(23*32, 17*56, 2, 11)
    floor_10 = Entities.Platform(27*32, 17*56, 2, 11)
    floor_11 = Entities.Platform(24*32, 18*56, 4, 9)

    floor_12 = Entities.Platform(16*32, 20*56, 3, 8)
    floor_13 = Entities.Platform(14*32, 21*56, 3, 7)

    floor_14 = Entities.Platform(5*32, 22*56, 2, 5)
    floor_15 = Entities.Platform(9*32, 22*56, 2, 5)
    floor_16 = Entities.Platform(6*32, 23*56, 4, 4)

    spikebox_0 = Entities.spike_box(0*32, 10*56 - 24)


    spikebox_1 = Entities.spike_box(5*32 + 8, 7*56 - 24)
    spikebox_1 = Entities.spike_box(7*32, 7*56 - 24)
    
    spikebox_2 = Entities.spike_box(12*32 + 8, 9*56 - 24)
    spikebox_2 = Entities.spike_box(14*32, 9*56 - 24)
    
    spikebox_3 = Entities.spike_box(21*32 + 8, 9*56 - 24)
    spikebox_3 = Entities.spike_box(23*32, 9*56 - 24)

    spikebox_4 = Entities.spike_box(25*32 - 8, 17*56 - 24)
    spikebox_5 = Entities.spike_box(14*32 + 2, 20*56 - 24)
    spikebox_6 = Entities.spike_box(7*32 - 8, 22*56 - 24)

    
    #render thingses
    #troll = Entities.Troll(38*32,20*32, True, (37*32, 48*32), (37*32, 22*32 - 64, 11*32, 2*32))
    #wiki = Entities.Wikipedia(55*32 + 16, 17*32, 3*32)
    goalpiece = Entities.goal_piece(1*32 + 16, 21*56)
        
    
    #other stuff
    Globals.player = Entities.Player(3*32,5*56)
    Globals.hud = Entities.hud()
    Globals.camera.xbounds = (0, 41*32)
    Globals.camera.ybounds = (0, 30*56)
    Globals.camera.y = 0
    killborder = Entities.kill_border((0,Globals.camera.ybounds[1]), (70*32,128))    
    
    bg = Entities.Background(functions.get_image(os.path.join('Resources','Stage 1 Resources','BackgroundStage1.bmp'), (255,0,255)), 42*32, 30*56)
 
def level_2():  
    
    #render floors
    floor_1 = Entities.Platform(53*32, 17*56, 8, 10)
    floor_1 = Entities.Platform(40*32, 15*56, 11, 12)
    floor_1 = Entities.Platform(37*32, 13*56, 1, 1)

    floor_1 = Entities.Platform(32*32, 12*56, 4, 15)
    
    floor_1 = Entities.Platform(27*32, 13*56, 1, 1)
    floor_1 = Entities.Platform(22*32, 14*56, 1, 1)

    floor_1 = Entities.Platform(17*32, 15*56, 3, 8)
    floor_1 = Entities.Platform(13*32, 15*56, 5, 3)

    floor_1 = Entities.Platform(3*32, 0*56, 4, 23)
    floor_1 = Entities.Platform(6*32, 21*56, 12, 2)




    spikebox_0 = Entities.spike_box(0*32, 10*56 - 24)

    
    #render thingses
    #troll = Entities.Troll(38*32,20*32, True, (37*32, 48*32), (37*32, 22*32 - 64, 11*32, 2*32))
    #wiki = Entities.Wikipedia(55*32 + 16, 17*32, 3*32)
    goalpiece = Entities.goal_piece(14*32, 19*56)
        
    
    #other stuff
    Globals.player = Entities.Player(8*32,17*56)
    Globals.hud = Entities.hud()
    Globals.camera.xbounds = (0, 70*32)
    Globals.camera.ybounds = (0, 30*56)
    Globals.camera.y = 0
    killborder = Entities.kill_border((0,Globals.camera.ybounds[1]), (70*32,128))    
    
    bg = Entities.Background(functions.get_image(os.path.join('Resources','Stage 1 Resources','BackgroundStage1.bmp'), (255,0,255)), 71*32, 30*56)
    
def boss_1():
    floor_platform = Entities.Platform(0*32, 12*32, 25, 5)
    Globals.player = Entities.Player(32*4,32*10)
    Globals.hud = Entities.hud()
    Globals.camera.xbounds = (0, 800)
    Globals.camera.ybounds = (0, 640)
    boss= Entities.InternetBoss(16*32, 6*32)