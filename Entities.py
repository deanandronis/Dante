'''
Created on Oct 27, 2013

@author: Dean, God Almighty of Sex and Women
'''

import pygame, sys, os
from pygame.locals import *
import functions, Constants, Globals


class Entity(pygame.sprite.Sprite):
    def __init__(self, *args):
        pygame.sprite.Sprite.__init__(self, *args)
        
#Player class
class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, Globals.group_PLAYER) #adds the player to the group Globals.group_PLAYER
        #Global variables for Character
        self.startpoint = (x,y) #starting location of the character
        self.xvel = 0 #horizontal velocity 
        self.yvel = 0 #vertical velocity
        self.health = 10 #player's health
        self.touching_ground = False #touching ground variable
        self.facing_right = True #variable for player direction
        self.next_level = False #variable to check for next level

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
        self.images = functions.load_imageset(self.imagepaths) #populates self.images with a dictionary of the above images with format 'imagename':image
        #set the current image to the loaded one
        self.imageindex = 0
        self.imagename = 'idleR'
        self.image = self.images[self.imagename][0]
        self.numimages = len(self.images[self.imagename]) - 1
        
        #add the collision box
        self.rect = pygame.Rect(self.image.get_rect()) #set the collision box bounds to player's image
        self.rect.x = x #set the collision box location
        self.rect.y = y
        self.x = self.rect.x #variable for temporarily storing location
        self.y = self.rect.y
        
    def update(self):
        self.touching_ground = False #assume not touching ground unless colliding later on
        self.rect = pygame.Rect(self.image.get_rect()) #set the collision box bounds to player's image
        self.rect.move_ip(self.x, self.y) #set the collision box location
        
        #move x and check for collision
        self.rect.x += self.xvel
        block_hit_list = pygame.sprite.spritecollide(self, Globals.group_COLLIDEBLOCKS, False) #create a list full of all blocks that player is colliding with
        for block in block_hit_list: #iterate through the list
            #Collision moving right means that player collided with left side of block
            if self.xvel > 0:
                self.rect.right = block.rect.left #set right side of player to left side of block
            elif self.xvel < 0:
                #Collision moving left means player collided with right side of block
                self.rect.left = block.rect.right #set left side of player to right side of block
        
        #apply gravity
        if self.yvel < 10:
            self.yvel += abs(self.yvel) / 40 + 0.36
        #move y and check for collisions
        self.rect.y += self.yvel
        block_hit_list = pygame.sprite.spritecollide(self, Globals.group_COLLIDEBLOCKS, False) #create list of blocks that player is colliding with  
        for block in block_hit_list: #iterate over list
            # check collision
            if self.yvel > 0: #top collision
                self.rect.bottom = block.rect.top #set bottom of player to top of block
                self.yvel = 0 #stop vertical movement
                self.onGround = True #player is on ground
            elif self.yvel < 0: #bottom collision
                self.rect.top = block.rect.bottom  #set the top of the player to the bottom of block
                self.yvel = 0 #stop vertical movement
                
       
        for item in Globals.group_SPECIAL: #iterate through special items
            if isinstance(item, hud) and self.rect.colliderect(item.rect): #if player is colliding with the hud
                self.reset() #reset position 
                self.health -= 3 #damage
                
                
        if not self.touching_ground: #check to see if player is within 20 pixels of a ground block 
            for item in Globals.group_COLLIDEBLOCKS:
                if self.rect.y < item.rect.y + item.rect.height and item.rect.y - 20 < self.rect.y + self.rect.height and self.rect.x + self.rect.width > item.rect.x and self.rect.x < item.rect.x + item.rect.width:
                    self.touching_ground = True
        
        #determine sprite set
        if self.touching_ground == True: #set of ground sprites
            if self.xvel > 0: #sprite should be running right
                if not self.imagename == 'runR':
                    self.change_image('runR')
                    self.facing_right = True
            elif self.xvel < 0: #sprite should be running left
                if not self.imagename == 'runL':
                    self.change_image('runL')
                    self.facing_right = False
            else: #player is stationary; check direction for sprite
                if self.facing_right == True: #sprite should be idling right
                    if not self.imagename == 'idleR':
                        self.change_image('idleR')
                        self.facing_right = True
                elif self.facing_right == False: #sprite should be idling left
                    if not self.imagename == 'idleL':
                        self.change_image('idleL')
                        self.facing_right = False
        else: #set of mid-air sprites
            if self.xvel > 0: #sprite should be jumping right
                if not self.imagename == "jumpR":
                        self.change_image('jumpR')
                        self.facing_right = True
            elif self.xvel < 0: #sprite should be jumping left
                if not self.imagename == 'jumpL':
                        self.change_image('jumpL')
                        self.facing_right = False
            else: #check direction player is facing
                if self.facing_right == True: #sprite should be jumping right
                    if not self.imagename == "jumpR":
                        self.change_image('jumpR')
                        self.facing_right = True
                else: #sprite should be jumping left
                    if not self.imagename == 'jumpL':
                        self.change_image('jumpL')
                        self.facing_right = False
        
        #set position
        self.x = self.rect.x
        self.y = self.rect.y
        
        
    def animate(self):
        self.image = self.images[self.imagename][self.imageindex] #rotate through list of animation sprites
        if self.imageindex == self.numimages: self.imageindex = 0 #if the sprite is at the end of the list, go to the start of the list
        else: self.imageindex += 1  #otherwise, allow the next rotation
        

    def reset(self):
        self.rect.x = self.startpoint[0] #go back to the start point
        self.rect.y = self.startpoint[1] 
        self.xvel= 0 #stop velocities
        self.yvel = 0
        
    
    def change_image(self, image):
        self.imageindex = 0 #reset the image position
        self.imagename = image #change the image list
        self.image = self.images[self.imagename][0] #set the image to the first image in the list
        self.numimages = len(self.images[self.imagename]) - 1 #set the length of the list

        
class Platform(Entity):
    def __init__(self, x, y, blocksacross, blocksdown): 
        #get image
        Entity.__init__(self, Globals.group_COLLIDEBLOCKS) 
        self.blockimage = functions.get_image(os.path.join('Resources','Stage 1 Resources','LevelTiles','1Floortile1.png'), (255,0,255))
        self.image = pygame.Surface((blocksacross*32,blocksdown*32))
        for rows in range(0,blocksdown):
            for columns in range(0,blocksacross):
                self.image.blit(self.blockimage, (columns*32,rows*32))
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(x,y)
        self.pos = (self.rect.x, self.rect.y)
        
        
class goal_piece(Entity):
    def __init__(self, x, y, stage):
        Entity.__init__(self, Globals.group_SPECIAL) #add the block to the Globals.group_SPECIAL group
        if stage == 1:
            self.image = functions.get_image(os.path.join('Resources','Stage 1 Resources', '1ObjectiveTile.bmp'), (255,0,255)) #load the image
            
        self.rect = pygame.Rect(self.image.get_rect()) #set the collision box to fit the image
        self.rect.move_ip((x,y)) #move the collision box into position
        

class Camera():
    def __init__(self):
        self.x = 0 #set the position of the camera
        self.y = 0
        self.width = 800 #set the size of the view window
        self.height = 640
        self.xbounds = (0, 992) #set the horizontal boundaries (min, max)
        self.ybounds = (0, 640) #set the vertical boundaries (min, max)
    
    def reset(self):
        self.x = 0 #set the position back to the start of the level
        self.y = 0
    
    def setSize(self, width, height): #change the view window's size
        self.width = width
        self.height = height
    
    def updatecamera(self, player): #check to see if the player is within the camera's window
        if player.rect.x + player.xvel > self.x + self.width*3/5: #if the player is in the right 2/5 of the window, move the camera
            self.x = player.rect.x - self.width*3/5
        elif player.rect.x + player.xvel < self.x + self.width*2/5: #if the player is in the left 2/5 of the window, move the camera
            self.x = player.rect.x - self.width*2/5
        
        if self.x + self.width> self.xbounds[1]: #check to see if the camera is within boundaries
            self.x = self.xbounds[1] - self.width
        elif self.x < self.xbounds[0]:
            self.x = self.xbounds[0]
        if self.y > self.ybounds[1]:
            self.y = self.ybounds[1] + self.height
        elif self.y < self.ybounds[0]:
            self.y = self.ybounds[0]
      
       

class hud(pygame.sprite.Sprite):
    def __init__(self, stage):
        pygame.sprite.Sprite.__init__(self, Globals.group_SPECIAL) #add the HUD to the Globals.group_SPECIAL group
        self.x = 0 #set the position of the HUD
        self.y = 544
        self.pos = (self.x,self.y) 
        if stage == 1:
            self.image = functions.get_image(os.path.join('Resources','Stage 1 Resources','1HUDBar.png'), (255,255,255)) #load the image
        self.image = pygame.transform.scale(self.image, (800,96)) #scale the image to the window size
        self.backimagestore = self.image #create a backup of the background image
        self.rect = pygame.Rect(self.image.get_rect()) #set the collision box to fit the image
        self.rect.move_ip(self.x, self.y) #move the collision box into position
        self.healthtext = Constants.healthtext.render('Health: ', 0, (255,253,255)) #load the text for the HUD
        
        #load relevant images
        self.imageloc = os.path.join('Resources','General Resources') #set the location for images
        self.imagepaths = {   'maxPortrait':(self.imageloc, 'Portrait', 0), 
                              
                          }
        self.images = {}
        self.images = functions.load_imageset(self.imagepaths) #load the images from the dictionary
        self.images['maxPortrait'][0] = pygame.transform.scale(self.images['maxPortrait'][0], (58,58)) #scale the portrait to fit the HUD
    
    def update(self, health): #redraw the HUD
        self.image = self.backimagestore #reset the image
        self.image.blit(self.healthtext, (100,38)) #draw the health text onto the HUD
        for i in range(0, health):
            pygame.draw.rect(self.image, (0,255,0), pygame.Rect(180 + i*21, 37, 14,22)) #draw the green health blocks
        for i in range(health, 10):
            pygame.draw.rect(self.image, (255,0,0), pygame.Rect(180 + i*21, 37, 14,22)) #draw the red health blocks
        self.image.blit(self.images['maxPortrait'][0], (19,17)) #draw the portrait onto the HUD

        