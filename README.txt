'''
Created on 31/10/2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, os, sys, Entities, functions, Constants, Globals, math, random
from random import randrange, randint

def load_title():
        bg = Entities.Menu_BG(functions.get_image(os.path.join('Resources','General Resources','TitleScreenFinal.png'), (0,0,0)))
        playbutt = Entities.Menu_PlayButt(359,330)
        quitbutt = Entities.Menu_QuitButt(359,450)
