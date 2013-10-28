'''
Created on Oct 27, 2013

@author: Dean, God Almighty of Sex and Women
'''

import pygame, sys, os
from pygame.locals import *
import functions

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
#Player class
class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        #Global variables for Character
        self.pos = (self.x,self.y) = x,y
        self.xvel = 0
        self.yvel = 0
        self.gravity = 2
        
        
        #load images
        '''
        IMAGE SYNTAX FOR USE:
        imageindex = 0
        imagename = (imagename)
        image = images[imagename][imageindex]
        numimages = len(images[imagename]) - 1
        '''
        self.imageloc = os.path.join('Resources','Max Bo','Bitmap')
        self.imagepaths = {   'runL':(os.path.join(self.imageloc,'RunningL'), 'RunningL', 8),
                              'runR':(os.path.join(self.imageloc,'RunningR'), 'RunningR', 8),
                              'idleL':(os.path.join(self.imageloc,'IdlingL'), 'idlingL', 19),
                              'idleR':(os.path.join(self.imageloc,'IdlingR'), 'idlingR', 19),
                              'jumpL':(os.path.join(self.imageloc,'JumpL'), 'jumpL', 0),
                              'jumpR':(os.path.join(self.imageloc,'JumpR'), 'jumpR', 0),
                          }
        self.images = {}
        self.images = functions.load_imageset(self.imagepaths)
        self.imageindex = 0
        self.imagename = 'idleR'
        self.image = self.images[self.imagename][0]
        self.numimages = len(self.images[self.imagename]) - 1
        
        
            
    def update(self):
        self.x += self.xvel
        self.y += self.yvel
        self.pos = (self.x, self.y)
    
    def animate(self):
        self.image = self.images[self.imagename][self.imageindex]
        if self.imageindex == self.numimages: self.imageindex = 0
        else: self.imageindex += 1  

    def check_collisions(self):
        pass
    