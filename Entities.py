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
        self.gravity = 40
        self.touching_ground = False
        self.facing_right = True
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
                              'deathL':(os.path.join(self.imageloc, 'DeathL'), 'DeathL', 30),
                              'deathR':(os.path.join(self.imageloc, 'DeathR'), 'DeathR', 30),
                              'slashL':(os.path.join(self.imageloc, 'NailslashL'), 'NailslashL', 13),
                              'slashR':(os.path.join(self.imageloc, 'NailslashR'), 'NailslashR', 13),
                              'spinL':(os.path.join(self.imageloc, 'spinL'), 'spinL', 19),
                              'spinR':(os.path.join(self.imageloc, 'spinR'), 'spinR', 19),
                              'shoutL':(os.path.join(self.imageloc, 'shoutL'), 'shoutL', 7),
                              'shoutR':(os.path.join(self.imageloc, 'shoutR'), 'shoutR', 7),
                          }
        self.images = {}
        self.images = functions.load_imageset(self.imagepaths)
        self.imageindex = 0
        self.imagename = 'idleR'
        self.image = self.images[self.imagename][0]
        self.numimages = len(self.images[self.imagename]) - 1
        
        #add the collision box
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.pos)
        
    def update(self, leftrightlist, updownlist, alldirlist):
        #update the collision box of the character
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.pos)
        
        #add the items to be checked to lists
        leftrightcontainer = [x for x in leftrightlist if -50 < x.x or x.x < 50]
        updowncontainer = [x for x in updownlist if -50 < x.y or x.y < 50]
        alldircontainer = [x for x in alldirlist if -50 < x.y or x.y < 50 or -50< x.x or x.x < 50]
        
        self.touching_ground = False
        #check the items in the lists for their respective collisions
        for item in updowncontainer:
            if self.rect.colliderect(item.rect):
                if self.y < item.y: #collide top
                    self.y = item.y - self.image.get_height()
                    self.yvel = 0
                    self.gravity = 0
                    self.touching_ground = True
                else: #collide bottom
                    self.y = item.y + item.image.get_height()
                    self.yvel = 0
                    self.gravity = 40
                    self.touching_ground = False
            elif not item.y - 10 < self.y + self.image.get_height() and not item.y + 10 + item.image.get_height() > self.y:
                self.gravity = 40
        for item in leftrightcontainer:
            if self.rect.colliderect(item.rect):
                if self.x < item.x: #collide left
                    if not self.xvel < 0:
                        self.x = item.x - self.image.get_width()
                        self.xvel = 0
                else: #collide right
                    if not self.xvel > 0:
                        self.x = item.x + item.image.get_width()
                        self.xvel = 0
        for item in alldircontainer:
            if self.rect.colliderect(item.rect):
                block_threshold = [item.y - item.image.get_height()/6, item.y + item.image.get_height() / 2, item.y + item.image.get_height() /6]
                player_centre_upper = self.y + (self.image.get_height()/6)
                player_centre_lower = self.y + (self.image.get_height()/6) + self.image.get_height()
                
                if self.x + self.image.get_width() < item.x + item.image.get_width(): #left of centre
                    if player_centre_upper > block_threshold[0] and player_centre_upper < block_threshold[2]:
                        #left collision
                        if not self.xvel < 0:
                            self.x = item.x - self.image.get_width()
                            self.xvel = 0
                    
                    elif player_centre_lower > block_threshold[0] and player_centre_lower < block_threshold[2]:
                        #left collision
                        if not self.xvel < 0:
                            self.x = item.x - self.image.get_width()
                            self.xvel = 0
                    else:
                        if self.y < item.y:
                            #top collision
                            self.y = item.y - self.image.get_height()
                            self.yvel = 0
                            self.gravity = 0
                            self.touching_ground = True
                        else:
                            #bottom collision
                            self.y = item.y + item.image.get_height()
                            self.yvel = 0
                            self.gravity = 40
                    
                else: #right of centre
                    if self.y + (self.image.get_height()/6) > block_threshold[0] and self.y + self.image.get_height()/6 < block_threshold[2]:
                        #right collision
                        if not self.xvel > 0:
                            self.x = item.x + item.image.get_width()
                            self.xvel = 0
                        
                    elif player_centre_lower > block_threshold[0] and player_centre_lower < block_threshold[2]:
                        #left collision
                        if not self.xvel > 0:
                            self.x = item.x + item.image.get_width()
                            self.xvel = 0
                    else:
                        if self.y < item.y:
                            #top collision
                            self.y = item.y - self.image.get_height()
                            self.yvel = 0
                            self.gravity = 0
                            self.touching_ground = True
                        else:
                            #bottom collision
                            self.y = item.y + item.image.get_height()
                            self.yvel = 0
                            self.gravity = 40
                            
        if self.gravity == 0: self.touching_ground = True
        
        #determine sprite set
        if self.touching_ground == True:
            if self.xvel > 0:
                if not self.imagename == 'runR':
                    self.change_image('runR')
                    self.facing_right = True
            elif self.xvel < 0:
                if not self.imagename == 'runL':
                    self.change_image('runL')
                    self.facing_right = False
            else:
                if self.facing_right == True:
                    if not self.imagename == 'idleR':
                        self.change_image('idleR')
                        self.facing_right = True
                elif self.facing_right == False:
                    if not self.imagename == 'idleL':
                        self.change_image('idleL')
                        self.facing_right = False
        else:
            if self.facing_right == True:
                if not self.imagename == "jumpR":
                    self.change_image('jumpR')
            else:
                if not self.imagename == 'jumpL':
                    self.change_image('jumpL')
        
        #apply gravity
        if not self.gravity == 0 and not self.yvel > 10:
            self.yvel += abs(self.yvel) / self.gravity + 0.36
        
        #apply speeds and reset position
        self.x += self.xvel
        self.y += self.yvel
        self.pos = (self.x, self.y)
    
    def animate(self):
        self.image = self.images[self.imagename][self.imageindex]
        if self.imageindex == self.numimages: self.imageindex = 0
        else: self.imageindex += 1  

    def check_collisions(self):
        pass
    
    def change_image(self, image):
        self.imageindex = 0
        self.imagename = image
        self.image = self.images[self.imagename][0]
        self.numimages = len(self.images[self.imagename]) - 1

class collisionblockupdown(Entity):
    def __init__(self, x, y, stage, blocknumber):
        Entity.__init__(self)
        #Global variables 
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        if stage == 1:
            if blocknumber % 2 == 0: self.image = functions.get_image(os.path.join('Resources','Stage 1 Resources','LevelTiles','1WallTile1.png'), (255,255,255))
            else: self.image = functions.get_image(os.path.join('Resources','Stage 1 Resources','LevelTiles','1WallTile2.png'), (255,255,255))  
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.pos)
        
class collisionblockleftright(Entity):
    def __init__(self, x, y, stage, blocknumber):
        Entity.__init__(self)
        #Global variables 
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        if stage == 1:
            if blocknumber % 2 == 0: self.image = functions.get_image(os.path.join('Resources','Stage 1 Resources','LevelTiles','1FloorTile1.png'), (255,255,255))
            else: self.image = functions.get_image(os.path.join('Resources','Stage 1 Resources','LevelTiles','1FloorTile2.png'), (255,255,255))  
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.pos)
        
class collisionblockalldir(Entity):
    def __init__(self, x, y, stage, blocknumber):
        Entity.__init__(self)
        #Global variables 
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        if stage == 1:
            self.image = functions.get_image(os.path.join('Resources','Stage 1 Resources','LevelTiles','1StandingTile.png'), (255,255,255))
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.pos)