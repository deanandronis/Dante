'''
Created on Oct 27, 2013

@author: Dean, God Almighty of Sex and Women
'''

import pygame, sys, os, math, textwrap
from pygame.locals import *
import functions, Constants, Globals
from random import randrange, randint
#base class for shit
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
        self.attack = None
        self.attacking = False
        self.arrowkey_enabled = True
        self.can_attack = True

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
            if not self.attacking:
                if self.xvel > 0:
                    self.rect.right = block.rect.left #set right side of player to left side of block
                elif self.xvel < 0:
                    #Collision moving left means player collided with right side of block
                    self.rect.left = block.rect.right #set left side of player to right side of block
            elif self.imagename == 'spinL' or self.imagename == 'slashL' or self.imagename == 'shoutL':
                if self.rect.x > block.rect.x:
                    self.rect.left = block.rect.right
                else:
                    self.rect.right = block.rect.left
            elif self.imagename == 'spinR' or self.imagename == 'slashR' or self.imagename == 'shoutR':
                if self.rect.x < block.rect.x:
                    self.rect.right = block.rect.left
                else:
                    self.rect.left = block.rect.right
            
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
                spleen = movingtext(self.rect.x - 8, self.rect.y - 20, 0, -4,"MY SPLEEN!")
            elif isinstance(item, goal_piece) and self.rect.colliderect(item.rect):
                self.next_level = True
                item.kill()
            elif isinstance(item, damage_tile) and self.rect.colliderect(item.rect):
                self.health -= 1
                item.kill()
                spleen = movingtext(self.rect.x - 8, self.rect.y - 20, 0, -4,"MY SPLEEN!")
                
                
        if not self.touching_ground: #check to see if player is within 20 pixels of a ground block 
            for item in Globals.group_COLLIDEBLOCKS:
                if self.rect.y < item.rect.y + item.rect.height and item.rect.y - 20 < self.rect.y + self.rect.height and self.rect.x + self.rect.width > item.rect.x and self.rect.x < item.rect.x + item.rect.width:
                    self.touching_ground = True
        
        #determine sprite set
        if not self.attacking:
            if self.touching_ground: #set of ground sprites
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
        else:
            if self.attack == 'spin':
                if self.facing_right:
                    if not self.imagename == 'spinR':
                        self.change_image('spinR')
                        self.rect.x -= 14
                else:
                    if not self.imagename == 'spinL':
                        self.change_image('spinL')
                        self.rect.x -= 14
            elif self.attack == 'slash':
                if self.facing_right:
                    if not self.imagename == 'slashR':
                        self.change_image('slashR')
                        self.rect.x -= 14
                else:
                    if not self.imagename == 'slashL':
                        self.change_image('slashL')
                        self.rect.x -= 14
            elif self.attack == 'shout':
                if self.facing_right:
                    if not self.imagename == 'shoutR':
                        self.change_image('shoutR')
                else:
                    if not self.imagename == 'shoutL':
                        self.change_image('shoutL')
                        self.rect.x -= 14
        #set position
        self.x = self.rect.x
        self.y = self.rect.y
        if self.health < 0:
            self.health = 0
        
        
    def animate(self):
        self.image = self.images[self.imagename][self.imageindex] #rotate through list of animation sprites
        if self.imageindex == self.numimages: 
            if self.imagename == 'spinR':
                self.rect.x += 15
                self.x += 14
                self.change_image('idleR')
                self.attack = None
                self.attacking = False
                self.can_attack = True
                self.arrowkey_enabled = True
                self.create_projectile()
            elif self.imagename == 'spinL':
                self.rect.x += 14
                self.x += 14
                self.change_image('idleL')
                self.attack = None
                self.attacking = False
                self.can_attack = True
                self.arrowkey_enabled = True
                self.create_projectile()
            elif self.imagename == 'slashR':
                self.rect.x += 20
                self.x += 20
                self.change_image('idleR')
                self.attack = None
                self.attacking = False
                self.can_attack = True
                self.arrowkey_enabled = True
            elif self.imagename == 'slashL':
                self.rect.x += 19
                self.x += 19
                self.change_image('idleL')
                self.attack = None
                self.attacking = False
                self.can_attack = True
                self.arrowkey_enabled = True
            elif self.imagename == 'shoutL':
                self.rect.x += 19
                self.x += 19
                self.change_image('idleL')
                self.attack = None
                self.attacking = False
                self.can_attack = True
                self.arrowkey_enabled = True
                shoutproj = shoutProj(self.rect.x - 20, self.rect.y + 10, True)
            elif self.imagename == 'shoutR':
                self.rect.x += 0
                self.x += 0
                self.change_image('idleR')
                self.attack = None
                self.attacking = False
                self.can_attack = True
                self.arrowkey_enabled = True
                shoutproj = shoutProj(self.rect.x + self.rect.width - 3, self.rect.y + 8, False)
            else:
                self.imageindex = 0 #if the sprite is at the end of the list, go to the start of the list
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
    
    def create_projectile(self):
        self.projectiletype = randrange(1,7,1)
        if self.projectiletype == 1:
            if self.facing_right:
                self.degrees = float(randrange(1,1000,1)) / 1000
                self.magnitude = float(randrange(10,13))
                self.projxvel = math.cos(self.degrees) * self.magnitude 
                self.projyvel = -math.cos(self.degrees) * self.magnitude 
                piano = Piano(self.rect.x + self.rect.width, self.rect.y - 90, self.projxvel, self.projyvel)
            else:
                self.degrees = float(randrange(1,1000,1)) / 1000
                self.magnitude = float(randrange(10,13))
                self.projxvel = -math.cos(self.degrees) * self.magnitude 
                self.projyvel = -math.cos(self.degrees) * self.magnitude 
                piano = Piano(self.rect.x - 75, self.rect.y - 50, self.projxvel, self.projyvel)
        elif self.projectiletype == 2:
                if self.facing_right:
                    self.degrees = float(randrange(1,1000,1)) / 1000
                    self.magnitude = float(randrange(10,13))
                    self.projxvel = math.cos(self.degrees) * self.magnitude 
                    self.projyvel = -math.cos(self.degrees) * self.magnitude 
                    watermelon = Watermelon(self.rect.x + self.rect.width, self.rect.y - 20, self.projxvel, self.projyvel)
                else:
                    self.degrees = float(randrange(1,1000,1)) / 1000
                    self.magnitude = float(randrange(10,13))
                    self.projxvel = -math.cos(self.degrees) * self.magnitude 
                    self.projyvel = -math.cos(self.degrees) * self.magnitude 
                    watermelon = Watermelon(self.rect.x - 60, self.rect.y - 20, self.projxvel, self.projyvel)
        elif self.projectiletype == 3:
                if self.facing_right:
                    self.degrees = float(randrange(1,1000,1)) / 1000
                    self.magnitude = float(randrange(10,13))
                    self.projxvel = math.cos(self.degrees) * self.magnitude 
                    self.projyvel = -math.cos(self.degrees) * self.magnitude 
                    chair = Chair(self.rect.x + self.rect.width, self.rect.y - 20, self.projxvel, self.projyvel)
                else:
                    self.degrees = float(randrange(1,1000,1)) / 1000
                    self.magnitude = float(randrange(10,13))
                    self.projxvel = -math.cos(self.degrees) * self.magnitude 
                    self.projyvel = -math.cos(self.degrees) * self.magnitude 
                    chair = Chair(self.rect.x - 60, self.rect.y - 20, self.projxvel, self.projyvel)
        elif self.projectiletype == 4:
                if self.facing_right:
                    self.degrees = float(randrange(1,1000,1)) / 1000
                    self.magnitude = float(randrange(10,13))
                    self.projxvel = math.cos(self.degrees) * self.magnitude 
                    self.projyvel = -math.cos(self.degrees) * self.magnitude 
                    hat = Hat(self.rect.x + self.rect.width, self.rect.y - 20, self.projxvel, self.projyvel)
                else:
                    self.degrees = float(randrange(1,1000,1)) / 1000
                    self.magnitude = float(randrange(10,13))
                    self.projxvel = -math.cos(self.degrees) * self.magnitude 
                    self.projyvel = -math.cos(self.degrees) * self.magnitude 
                    hat = Hat(self.rect.x - 60, self.rect.y - 20, self.projxvel, self.projyvel)
        elif self.projectiletype == 5:
                if self.facing_right:
                    self.degrees = float(randrange(1,1000,1)) / 1000
                    self.magnitude = float(randrange(10,13))
                    self.projxvel = math.cos(self.degrees) * self.magnitude 
                    self.projyvel = -math.cos(self.degrees) * self.magnitude 
                    book = Book(self.rect.x + self.rect.width, self.rect.y - 20, self.projxvel, self.projyvel)
                else:
                    self.degrees = float(randrange(1,1000,1)) / 1000
                    self.magnitude = float(randrange(10,13))
                    self.projxvel = -math.cos(self.degrees) * self.magnitude 
                    self.projyvel = -math.cos(self.degrees) * self.magnitude 
                    book = Book(self.rect.x - 60, self.rect.y - 20, self.projxvel, self.projyvel)
        elif self.projectiletype == 6:
                if self.facing_right:
                    self.degrees = float(randrange(1,1000,1)) / 1000
                    self.magnitude = float(randrange(10,13))
                    self.projxvel = math.cos(self.degrees) * self.magnitude 
                    self.projyvel = -math.cos(self.degrees) * self.magnitude 
                    tv = Television(self.rect.x + self.rect.width, self.rect.y - 20, self.projxvel, self.projyvel)
                else:
                    self.degrees = float(randrange(1,1000,1)) / 1000
                    self.magnitude = float(randrange(10,13))
                    self.projxvel = -math.cos(self.degrees) * self.magnitude 
                    self.projyvel = -math.cos(self.degrees) * self.magnitude 
                    tv = Television(self.rect.x - 60, self.rect.y - 20, self.projxvel, self.projyvel)

#collision shit
class Platform(Entity):
    def __init__(self, x, y, blocksacross, blocksdown): 
        #get image
        Entity.__init__(self, Globals.group_COLLIDEBLOCKS) 
        if Globals.stage == 1:
            self.blockimage = functions.get_image(os.path.join('Resources','Stage 1 Resources','LevelTiles','1Floortile1.png'), (255,0,255))
        self.image = pygame.Surface((blocksacross*32,blocksdown*32))
        for rows in range(0,blocksdown):
            for columns in range(0,blocksacross):
                self.image.blit(self.blockimage, (columns*32,rows*32))
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(x,y)
        self.pos = (self.rect.x, self.rect.y)
        
class damage_tile(Entity):
    def __init__(self,x,y):
        Entity.__init__(self, Globals.group_SPECIAL) #add the block to its group
        if Globals.stage == 1:
            self.image = functions.get_image(os.path.join('Resources','Stage 1 Resources','LevelTiles','1DeathTile.png'), (255,0,255))
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip((x,y))
        
class goal_piece(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, Globals.group_SPECIAL) #add the block to the Globals.group_SPECIAL group
        if Globals.stage == 1:
            self.image = functions.get_image(os.path.join('Resources','Stage 1 Resources', '1ObjectiveTile.bmp'), (255,0,255)) #load the image
            
        self.rect = pygame.Rect(self.image.get_rect()) #set the collision box to fit the image
        self.rect.move_ip((x,y)) #move the collision box into position
        
#game essentials
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
        
        if self.x + self.width > self.xbounds[1]: #check to see if the camera is within boundaries
            self.x = self.xbounds[1] - self.width
        elif self.x <= self.xbounds[0]:
            self.x = self.xbounds[0]
        if self.y > self.ybounds[1]:
            self.y = self.ybounds[1] + self.height
        elif self.y < self.ybounds[0]:
            self.y = self.ybounds[0]
         

class hud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, Globals.group_SPECIAL) #add the HUD to the Globals.group_SPECIAL group
        self.x = 0 #set the position of the HUD
        self.y = 544
        self.pos = (self.x,self.y) 
        if Globals.stage == 1:
            self.image = functions.get_image(os.path.join('Resources','Stage 1 Resources','1HUDBar.png'), (255,255,255)) #load the image
        self.image = pygame.transform.scale(self.image, (800,96)) #scale the image to the window size
        self.backimagestore = self.image #create a backup of the background image
        self.rect = pygame.Rect(self.image.get_rect()) #set the collision box to fit the image
        self.rect.move_ip(self.x, self.y) #move the collision box into position
        self.healthtext = Constants.healthtext.render('Health: ', 0, (255,253,255)) #load the text for the HUD
        
        #load relevant images
        self.imageloc = os.path.join('Resources','General Resources','HUD') #set the location for images
        self.imagepaths = {   'maxPortrait':(self.imageloc, 'Bo', 3), 
                              
                          }
        self.images = {}
        self.images = functions.load_imageset(self.imagepaths) #load the images from the dictionary
        #self.images['maxPortrait'][0] = pygame.transform.scale(self.images['maxPortrait'][0], (58,58)) #scale the portrait to fit the HUD
    
    def update(self, health): #redraw the HUD
        self.image = self.backimagestore #reset the image
        self.image.blit(self.healthtext, (100,38)) #draw the health text onto the HUD
        for i in range(0, health):
            pygame.draw.rect(self.image, (0,255,0), pygame.Rect(180 + i*21, 37, 14,22)) #draw the green health blocks
        for i in range(health, 10):
            pygame.draw.rect(self.image, (255,0,0), pygame.Rect(180 + i*21, 37, 14,22)) #draw the red health blocks
        #draw the portrait onto the HUD
        if health > 7: self.image.blit(self.images['maxPortrait'][0], (19,17)) 
        elif health > 4: self.image.blit(self.images['maxPortrait'][1], (19,17))
        elif health > 1: self.image.blit(self.images['maxPortrait'][2], (19,17))
        elif health <= 1: self.image.blit(self.images['maxPortrait'][3],(19,17))
        
#projectile classes        
class Projectile(Entity):
    def __init__(self, x, y, xvel, yvel):
        Entity.__init__(self, Globals.group_PROJECTILES)
    
        #set the required variables    
        self.xvel = xvel
        self.yvel = yvel
        self.gravity = True
        self.numbounce = 0
    def update(self):
        self.rect.x += self.xvel
        if self.gravity: self.yvel += abs(self.yvel)/40 + 0.36
        self.rect.y += self.yvel
        self.collidearray = pygame.sprite.spritecollide(self, Globals.group_COLLIDEBLOCKS, False)
        for item in self.collidearray:
            if self.rect.x < item.rect.x or self.rect.y > item.rect.y:
                self.kill()
            else:
                if self.numbounce < 2:
                    self.yvel /= -2
                    self.rect.y -= 15
                    self.numbounce += 1
                else:
                    self.kill()
                    
                
        if pygame.sprite.spritecollide(self,Globals.group_PLAYER, False):
            self.kill()
            self.yvel = 0
        elif pygame.sprite.spritecollide(self, Globals.group_SPECIAL, False):
            self.kill()
            self.yvel = 0
               
class Piano(Projectile):
    def __init__(self, x, y, xvel, yvel):
        self.image = functions.get_image(os.path.join('Resources','Projectiles','PianoProjectile1.png'), (255,0,255)) #get the piano image
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = x
        self.rect.y = y
        Projectile.__init__(self, x, y, xvel, yvel)
        self.damage = 6
        
        
class Watermelon(Projectile):
    def __init__(self, x, y, xvel, yvel):
        self.image = functions.get_image(os.path.join('Resources','Projectiles','WatermelonProjectile1.png'), (255,0,255)) #get the piano image
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = x
        self.rect.y = y
        Projectile.__init__(self, x, y, xvel, yvel)
        self.damage = 4  
        

class Hat(Projectile):
    def __init__(self, x, y, xvel, yvel):
        self.image = functions.get_image(os.path.join('Resources','Projectiles','HatProjectile.png'), (255,0,255)) #get the piano image
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = x
        self.rect.y = y
        Projectile.__init__(self, x, y, xvel, yvel)   
        self.damage = 1

class Book(Projectile):
    def __init__(self, x, y, xvel, yvel):
        self.image = functions.get_image(os.path.join('Resources','Projectiles','BookProjectile.png'), (255,0,255)) #get the piano image
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = x
        self.rect.y = y
        Projectile.__init__(self, x, y, xvel, yvel)   
        self.damage = 2
        
        
class Television(Projectile):
    def __init__(self, x, y, xvel, yvel):
        self.imagelist = functions.create_image_list(os.path.join('Resources','Projectiles','Bitmap','TV'), 'TV', 17, '.bmp', (255,0,255))
        self.image = self.imagelist[0]
        self.numimages = 17
        self.image_index = 0
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = x
        self.rect.y = y
        Projectile.__init__(self, x, y, xvel, yvel)
        self.damage = 5   
    def animate(self):
        self.image = self.imagelist[self.image_index]
        if self.image_index < self.numimages: self.image_index += 1
        else: self.image_index = 0
        
class Chair(Projectile):
    def __init__(self, x, y, xvel, yvel):
        self.image = functions.get_image(os.path.join('Resources','Projectiles','chair.png'), (255,0,255)) #get the piano image
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = x
        self.rect.y = y
        Projectile.__init__(self, x, y, xvel, yvel)   
        self.damage = 3
        

class shoutProj(Projectile):
    def __init__(self, x, y, attack_left):
        self.imagelist = functions.create_image_list(os.path.join('Resources','Projectiles','Bitmap','Gaypride'), 'Gaypride',8, '.bmp', (255,0,255))
        self.image = self.imagelist[0]
        self.image_index = 0
        self.numimages = 8
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = x
        self.rect.y = y
        if attack_left:
            Projectile.__init__(self, x, y, -7, 0)
        else:
            Projectile.__init__(self,x,y,7,0)
        self.gravity = False
            
    def animate(self):
        self.image = self.imagelist[self.image_index]
        if self.image_index < self.numimages: self.image_index += 1
        else: self.image_index = 0
        
class movingtext(Entity):
    def __init__(self, x, y, xvel, yvel, text):
        Entity.__init__(self, Globals.group_SPECIAL)
        self.xvel = xvel
        self.yvel = yvel
        self.image = Constants.spleentext.render(text, 0, (255,253,255)) #load the text 
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(x,y)
        
    def update(self):
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        
        if pygame.sprite.spritecollide(self, Globals.group_COLLIDEBLOCKS, False):
            self.kill()
        if self.rect.x < 0 or self.rect.x > 1000 or self.rect.y < 0 or self.rect.y > 1000:
            self.kill()

class narrator_bubble(Entity):
    def __init__(self, x, y, text):
        Entity.__init__(self, Globals.group_SPECIAL)
        self.rendertext = []
        self.images = [functions.get_image(os.path.join('Resources','General Resources','HUD','messagebubbleleft.bmp'), (255,0,255)),
                       functions.get_image(os.path.join('Resources','General Resources','HUD','messagebubble_centre.bmp'), (255,0,255)),
                       functions.get_image(os.path.join('Resources','General Resources','HUD','messagebubbleright.bmp'), (255,0,255))
                       ]
        self.text = textwrap.dedent(text) 
        self.bubblewidth = len(text)*3
        if self.bubblewidth <70: self.bubblewidth = 70
        self.maxwidth = self.bubblewidth         
        self.image=pygame.Surface((self.bubblewidth+11+55, 84))
        self.text = textwrap.wrap(self.text, self.image.get_width()/8 - 1)
        for item in self.text:
            self.rendertext.append(Constants.narratetext.render(item, 0, (0 ,0,0))) #load the text
        self.image.blit(self.images[0], (0,0))
        
        for i in range(0,self.bubblewidth):
            self.image.blit(self.images[1],(i + 11, 0))
        self.image.blit(self.images[2],(self.image.get_width() - 55,0))
        for index, item in enumerate(self.rendertext):
            self.image.blit(item, (12, 11 + index * 14))
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(x,y)
        
class Troll(Entity):
    def __init__(self, x, y, facingL):
        Entity.__init__(self, Globals.group_AI)
        #load images
        self.imageloc = os.path.join('Resources','Stage 1 Resources','Troll','Bitmaps')
        self.imagepaths = {   'walkL':(os.path.join(self.imageloc,'WalkL'), 'TrollWalkL', 3),
                              'walkR':(os.path.join(self.imageloc,'WalkR'), 'TrollWalkR', 3),
                              'idleL':(os.path.join(self.imageloc,'WalkL'), 'TrollWalkL', 0),
                              'idleR':(os.path.join(self.imageloc,'WalkR'), 'TrollWalkR', 0),
                              'explodeL':(os.path.join(self.imageloc,'ExplodeL'), 'TrollExplodeL', 9),
                              'explodeR':(os.path.join(self.imageloc,'ExplodeR'), 'TrollExplodeR', 9)
                          }
        self.images = {}
        self.images = functions.load_imageset(self.imagepaths) #populates self.images with a dictionary of the above images with format 'imagename':image
        #set image
        if facingL: 
            self.image = self.images['idleL'][0]
            self.numimages = len(self.images['idleL']) - 1
            self.imagename = 'idleL'
        else: 
            self.image = self.images['idleR'][0]
            self.numimages = len(self.images['idleR']) - 1
            self.imagename = 'idleR'
        self.image_index = 0
        
        #declare variables
        self.facingL = facingL
        self.xvel = 0
        self.yvel = 0
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip((x,y))
        self.range_to_character = 0
        self.wall_separating = False
        self.health = 3
        self.eventcounter = 5
        
    
        
    def animate(self):
        self.image = self.images[self.imagename][self.image_index]
        if self.image_index < self.numimages: self.image_index += 1
        else: self.image_index = 0
    
    def update(self, screen):
        pass    
        
    def calculate_range(self):
        self.player.x = Globals.player.rect.x 
        self.player.y = Globals.player.rect.y
        #calc horizontal and vertical distances
        if self.rect.x > self.player.x: self.xdist_to_character = self.rect.x - self.player.x
        else: self.xdist_to_character = self.player.x - self.rect.x
        if self.rect.y > self.player.y: self.ydist_to_character = self.rect.y - self.player.y
        else: self.ydist_to_character = self.player.y - self.rect.y
        
        #calculate overall distance
        self.dist_to_character = math.sqrt((self.ydist_to_character^2)+(self.xdist_to_character*2))
        self.angle_to_character = math.atan2(self.ydist_to_character, self.xdist_to_character)
        return [self.dist_to_character, self.angle_to_character]
        
        
            
        