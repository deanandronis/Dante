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
        self.keys = {'left':False, 'right':False}
        self.startpoint = (x,y) #starting location of the character
        self.xvel = 0.0 #horizontal velocity 
        self.yvel = 0.0 #vertical velocity
        self.health = 10 #player's health
        self.touching_ground = False #touching ground variable
        self.facing_right = True #variable for player direction
        self.next_level = False #variable to check for next level
        self.attack = None
        self.attacking = False
        self.arrowkey_enabled = True
        self.can_attack = True
        self.slash_damage = True
        self.leftdown = False
        self.rightdown = False
        self.slideduration = 0
        self.slidetimer = 0
        self.can_damage = True
        self.animatetimer = 6
        self.grav = True
        self.lock_midair = False
        
        #load images
        '''
        IMAGE SYNTAX FOR USE:
        imageindex = 0
        imagename = (imagename)
        image = images[imagename][imageindex]
        numimages = len(images[imagename]) - 1
        '''
        self.imageloc = os.path.join('Resources','New Max')
        self.imagepaths = {   'runL':(os.path.join(self.imageloc,'RunL'), 'RunL', 9),
                              'runR':(os.path.join(self.imageloc,'RunR'), 'RunR', 9),
                              'idleL':(os.path.join(self.imageloc,'IdleL'), 'idleL', 0),
                              'idleR':(os.path.join(self.imageloc,'IdleR'), 'idleR', 0),
                              'jumpL':(os.path.join(self.imageloc,'JumpL'), 'jumpL', 0),
                              'jumpR':(os.path.join(self.imageloc,'JumpR'), 'jumpR', 0),
                              'deathL':(os.path.join(self.imageloc, 'DieL'), 'DieL', 30),
                              'deathR':(os.path.join(self.imageloc, 'DieR'), 'DieR', 30),
                              'slashL':(os.path.join(self.imageloc, 'SlashL'), 'NailL', 13),
                              'slashR':(os.path.join(self.imageloc, 'SlashR'), 'NailR', 13),
                              'spinL':(os.path.join(self.imageloc, 'SpinL'), 'SpinL', 20),
                              'spinR':(os.path.join(self.imageloc, 'spinR'), 'spinR', 20),
                              'shoutL':(os.path.join(self.imageloc, 'shoutL'), 'shoutL', 15),
                              'shoutR':(os.path.join(self.imageloc, 'shoutR'), 'shoutR', 15),
                              'teabagL':(os.path.join(self.imageloc, 'teabagL'), 'teabagL', 0),
                              'teabagR':(os.path.join(self.imageloc, 'teabagR'), 'teabagR', 0),
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
        print self.lock_midair
        self.collidelist = [x for x in Globals.group_COLLIDEBLOCKS if x.rect.collidepoint(self.rect.centerx, self.rect.bottom + 1)]
        self.xvel = float(self.xvel)
        if self.rect.y > Globals.hud.rect.y:
            self.health -= 4
            self.reset()
            spleen = movingtext(self.rect.x - 8, self.rect.y - 20, 0, -4,"MY SPLEEN!")
        self.touching_ground = False #assume not touching ground unless colliding later on
        self.rect = pygame.Rect(self.image.get_rect()) #set the collision box bounds to player's image
        self.rect.move_ip(self.x, self.y) #set the collision box location
        #friction
        if self.collidelist:
            if self.xvel > -0.5 and self.xvel < 0.5 and not self.keys['left'] == True and not self.keys['right'] == True: 
                self.xvel = 0  
                self.lock_midair = False    
            self.touching_ground = True   
            
        #move x and check for collision
        self.rect.x += self.xvel
        self.check_x_coll()
        #apply gravity
        if self.yvel < 10 and self.grav:
            self.yvel += abs(self.yvel) / 40 + 0.36
           
        #move y and check for collisions
        self.rect.y += self.yvel
        self.check_y_coll()
        self.collide_SPECIAL()
                        
        for item in Globals.group_PROJECTILES:
            if self.rect.colliderect(item.rect) and isinstance(item, EnemyProj):
                self.health -= item.damage
                item.kill()
                
        #determine sprite set
        self.check_sprites()
        #set position
        self.x = self.rect.x
        self.y = self.rect.y
        if self.health < 0:
            self.health = 0
        
    def check_x_coll(self):
        block_hit_list = pygame.sprite.spritecollide(self, Globals.group_COLLIDEBLOCKS, False) #create a list full of all blocks that player is colliding with
        for block in block_hit_list: #iterate through the list
            #Collision moving right means that player collided with left side of block
            if not self.attacking:
                if self.xvel > 0:
                    self.rect.right = block.rect.left #set right side of player to left side of block
                    self.xvel = 0
                    self.keys['left'] = False
                    self.keys['right'] = False
                    
                elif self.xvel < 0:
                    #Collision moving left means player collided with right side of block
                    self.rect.left = block.rect.right #set left side of player to right side of block
                    self.xvel = 0
                    self.keys['left'] = False
                    self.keys['right'] = False
                    
            elif self.imagename == 'spinL' or self.imagename == 'slashL' or self.imagename == 'shoutL':
                if self.rect.x > block.rect.x:
                    self.rect.left = block.rect.right 
                    self.xvel = 0
                    self.keys['left'] = False
                    self.keys['right'] = False
                    
                else:
                    self.rect.right = block.rect.left 
                    self.xvel = 0
                    self.keys['left'] = False
                    self.keys['right'] = False
                    
            elif self.imagename == 'spinR' or self.imagename == 'slashR' or self.imagename == 'shoutR':
                if self.rect.x < block.rect.x:
                    self.rect.right = block.rect.left
                    self.xvel = 0
                    self.keys['left'] = False
                    self.keys['right'] = False
                    
                else:
                    self.rect.left = block.rect.right
                    self.xvel = 0
                    self.keys['left'] = False
                    self.keys['right'] = False
    
    def check_y_coll(self):
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
        
    def collide_SPECIAL(self):
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
            elif isinstance(item, key) and self.rect.colliderect(item.rect):
                item.destroy = True
                item.image = functions.get_image(os.path.join('Resources','General Resources','InvisibleTile.png'),(255,0,255))
            elif isinstance(item, Coin) and self.rect.colliderect(item.rect):
                Globals.score += 5
                item.kill()
        
    def animate(self):
        self.image = self.images[self.imagename][self.imageindex] #rotate through list of animation sprites
        if self.imageindex == self.numimages: 
            if self.imagename == 'spinR':
                self.rect.x += 8
                self.x += 8
                self.change_image('idleR')
                self.attack = None
                self.attacking = False
                self.can_attack = True
                self.arrowkey_enabled = True
                
            elif self.imagename == 'spinL':
                self.rect.x += 8
                self.x += 8
                self.change_image('idleL')
                self.attack = None
                self.attacking = False
                self.can_attack = True
                self.arrowkey_enabled = True
                
            elif self.imagename == 'slashR':
                self.rect.x += 20
                self.x += 20
                self.change_image('idleR')
                self.attack = None
                self.attacking = False
                self.can_attack = True
                self.arrowkey_enabled = True
            elif self.imagename == 'slashL':
                self.rect.x -= 3
                self.x -= 3
                self.change_image('idleL')
                self.attack = None
                self.attacking = False
                self.can_attack = True
                self.arrowkey_enabled = True
            elif self.imagename == 'shoutL' and self.attack == 'shout':
                self.rect.x += 3
                self.x += 3
                self.change_image('idleL')
                self.attack = None
                self.attacking = False
                self.can_attack = True
                self.arrowkey_enabled = True
                
            elif self.imagename == 'shoutR' and self.attack == 'shout':
                self.rect.x -= 3
                self.x -= 3
                self.change_image('idleR')
                self.attack = None
                self.attacking = False
                self.can_attack = True
                self.arrowkey_enabled = True
                
            elif self.imagename == "shoutR" and self.attack == 'lazer':
                self.change_image('idleR')
                self.attack = None
                self.attacking = False
                self.can_attack = True
                self.arrowkey_enabled = True
                self.rect.x -= 3
                self.x -= 3
                
            elif self.imagename == "shoutL" and self.attack == 'lazer':
                self.change_image('idleL')
                self.rect.x += 3
                self.x += 3
                self.attack = None
                self.attacking = False
                self.can_attack = True
                self.arrowkey_enabled = True
                
            elif self.imagename == "Teabag":
                self.change_image('teabag')
                self.attack = None
                self.attacking = False
                self.can_attack = False
                self.arrowkey_enabled = False
    
            else:
                self.imageindex = 0 #if the sprite is at the end of the list, go to the start of the list
        elif self.imagename == 'spinL' and self.imageindex == 15:
                self.create_projectile()
                self.imageindex += 1
            
        elif self.imagename == 'spinR' and self.imageindex == 15:
                self.create_projectile()
                self.imageindex += 1
        
        elif self.imagename == 'shoutL' and self.attack == 'lazer' and self.imageindex == 7:
            laser = lazer(self.rect.x + 6, self.rect.y + 15, True)
            self.imageindex += 1
        
        elif self.imagename == 'shoutR' and self.attack == 'lazer' and self.imageindex == 7:
            laser = lazer(self.rect.x + self.rect.width - 10, self.rect.y + 13, False)
            self.imageindex += 1
        
        elif self.imagename == 'shoutL' and self.attack == 'shout' and self.imageindex == 7:
            shoutproj = shoutProj(self.rect.x - 20, self.rect.y + 13, True)
            self.imageindex += 1
        
        elif self.imagename == 'shoutR' and self.attack == 'shout' and self.imageindex == 7:
            shoutproj = shoutProj(self.rect.x + self.rect.width - 1, self.rect.y + 13, False)
            self.imageindex += 1    
        
            
        else: self.imageindex += 1  #otherwise, allow the next rotation
   
    def check_sprites(self):
        if not self.attacking:
            if self.touching_ground: #set of ground sprites
                if not self.xvel == 0 and not self.keys['left'] == False and not self.keys['right'] == False:
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
                elif not self.xvel == 0 and self.keys['left'] == False and self.keys['right'] == False:
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
            
                else:
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
                if self.xvel == 0:
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
                        self.rect.x -= 8
                else:
                    if not self.imagename == 'spinL':
                        self.change_image('spinL')
                        self.rect.x -= 8
            elif self.attack == 'slash':
                if self.facing_right:
                    if not self.imagename == 'slashR':
                        self.change_image('slashR')
                        self.rect.x -= 3
                        self.slash_damage = True
                else:
                    if not self.imagename == 'slashL':
                        self.change_image('slashL')
                        self.rect.x -= 13
                        self.slash_damage = True
            elif self.attack == 'shout':
                if self.facing_right:
                    if not self.imagename == 'shoutR':
                        self.change_image('shoutR')
                        self.rect.x += 3
                else:
                    if not self.imagename == 'shoutL':
                        self.change_image('shoutL')
                        self.rect.x -= 4
            elif self.attack == 'lazer':
                if self.facing_right:
                    if not self.imagename == 'shoutR':
                        self.change_image('shoutR')
                        self.rect.x += 3
                else:
                    if not self.imagename == 'shoutL':
                        self.change_image('shoutL')
                        self.rect.x -= 4
                        
            elif self.attack == 'teabag':
                if self.facing_right:
                    if not self.imagename == 'teabagR':
                        self.change_image('teabagR')
                        self.rect.x += 3
                else:
                    if not self.imagename == 'teabagL':
                        self.change_image('teabagL')
                        self.rect.x -= 4
       
    def reset(self):
        self.rect.x = self.startpoint[0] #go back to the start point
        self.rect.y = self.startpoint[1] 
        self.x = self.rect.x
        self.y = self.rect.y
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

    def right_pressed(self):
        if self.arrowkey_enabled and not self.lock_midair:
                self.xvel = 3.5
                
    def left_pressed(self):
        if self.arrowkey_enabled and not self.lock_midair: 
                    self.xvel = -3.5
                    
    def left_released(self):
        if not self.xvel > 0 and self.arrowkey_enabled and not self.lock_midair: #set the player's horizontal velocity to 0 if player isn't moving right
                self.xvel = 0
                
    def right_released(self):
        if not self.xvel < 0 and self.arrowkey_enabled and not self.lock_midair: #set the player's horizontal velocity to 0 if player isn't moving left
            self.xvel = 0

#root classes
class Platform(Entity):
    def __init__(self, x, y, blocksacross, blocksdown): 
            #get image
            Entity.__init__(self, Globals.group_COLLIDEBLOCKS) 
            if Globals.stage == 1:
                self.imageloc = os.path.join('Resources','Stage 1 Resources','LevelTiles') #set the location for images
                self.images = [
                           functions.get_image(os.path.join(self.imageloc,'PlatformL_EdgeBot.bmp'), (255,0,255)),
                           functions.get_image(os.path.join(self.imageloc,'PlatformCentreBot1.bmp'), (255,0,255)),
                           functions.get_image(os.path.join(self.imageloc,'PlatformCentreBot2.bmp'), (255,0,255)),
                           functions.get_image(os.path.join(self.imageloc,'PlatformCentreBot3.bmp'), (255,0,255)),
                           functions.get_image(os.path.join(self.imageloc,'PlatformR_EdgeBot.bmp'), (255,0,255)),
                           functions.get_image(os.path.join(self.imageloc,'PlatformCentreBotFiller.bmp'), (255,0,255)),
                           functions.get_image(os.path.join(self.imageloc,'Floor_tile_single.png'), (255,0,255)),
                           ]
            self.image = pygame.Surface((blocksacross*32-16,blocksdown*56 + 8))
            if not blocksacross == 1:    
                for rows in range(0,blocksdown):
                    for columns in range(0,blocksacross):
                        if rows == 0 and columns == 0:
                            self.image.blit(self.images[0], (columns*32,rows*56))
                            top = platformback(columns*32 + x, rows * 32 + y, 0)
                        elif rows == 0 and columns == blocksacross - 1:
                            self.image.blit(self.images[4], (columns*32,rows*56))
                            top = platformback(columns*32 + x, rows * 32 + y, 2)
                        elif rows == 0 and columns%3 == 0:
                            self.image.blit(self.images[1], (columns*32,rows*56))
                            top = platformback(columns*32 + x, rows * 32 + y, 1)
                        elif rows == 0 and columns%3 == 1:
                            self.image.blit(self.images[2], (columns*32,rows*56))
                            top = platformback(columns*32 + x, rows * 32 + y, 1)
                        elif rows == 0 and columns%3 == 2:
                            self.image.blit(self.images[3], (columns*32,rows*56))
                            top = platformback(columns*32 + x, rows*56 + y, 1)
                        else:
                            self.image.blit(self.images[5], (columns*32,rows*56))
            else:
                self.image.blit(self.images[5], (0,0))
                for rows in range(0, blocksdown):
                    self.image.blit(self.images[4], (0,rows*56))
            self.co_friction = 1
            self.rect = pygame.Rect(x, y +8, blocksacross*32-16, blocksdown*56 - 8)
            self.pos = (self.rect.x, self.rect.y)
        
class platformback(Entity):
    def __init__(self, x, y, index):
        Entity.__init__(self, Globals.group_BACKTILES)     
        if index == 0:   
            self.image = functions.get_image(os.path.join('Resources','Stage 1 Resources','LevelTiles','PlatformL_EdgeTop.bmp'), (255,0,255))
        elif index == 1:
            self.image = functions.get_image(os.path.join('Resources','Stage 1 Resources','LevelTiles','PlatformCentreTop.bmp'), (255,0,255))
        elif index == 2:
            self.image = functions.get_image(os.path.join('Resources','Stage 1 Resources','LevelTiles','PlatformR_EdgeTop.bmp'), (255,0,255))
        self.pos = (x,y)
        
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
        
class key(Entity):
    def __init__(self, x, y, index):
        Entity.__init__(self, Globals.group_SPECIAL)
        self.image = functions.get_image(os.path.join('Resources','General Resources','KeyTile.bmp'), (255,0,255))
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip((x,y))
        self.destroy = False
        self.destroytimer = 30
        self.timer = 0
        self.pos = (self.rect.x, self.rect.y)
        self.index = index
    
    def update(self):
        if self.destroy:
            Globals.key_pause = True
            #self.rect.y = -1000
            self.timer += 1
            self.destroylist = [x for x in Globals.group_COLLIDEBLOCKS if isinstance(x, Door) and x.index == self.index]
            if self.destroylist and self.timer == self.destroytimer:
                
                self.destitem = self.destroylist[len(self.destroylist) - 1]
                if self.destitem.rect.width > self.destitem.rect.height: 
                    self.destitem.remove_one_horiz()
                else: 
                    self.destitem.remove_one_vert()
            elif not self.destroylist: 
                self.kill()
                Globals.key_pause = False
          
        if self.timer >= self.destroytimer: self.timer = 0
              
class Door(Entity):
    def __init__(self, x, y, blocksacross, blocksdown, index):
        Entity.__init__(self, Globals.group_COLLIDEBLOCKS)
        self.blockimage = functions.get_image(os.path.join('Resources','General Resources','Doortile.png'), (255,0,255))
        self.image = pygame.Surface((blocksacross*32,blocksdown*32))
        for rows in range(0,blocksdown):
            for columns in range(0,blocksacross):
                self.image.blit(self.blockimage, (columns*32, rows*32))
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(x,y)
        self.pos = (self.rect.x, self.rect.y)
        self.width = blocksacross*32
        self.height = blocksdown*32
        self.index = index
        self.co_friction = 1
    
    def remove_one_horiz(self):
        if self.width == 32: 
            self.kill()
        else:
            self.rect.x += 32
            self.width -= 32
            self.image = pygame.Surface((self.width, self.height))
            for rows in range(0,self.height/32):
                for columns in range(0,self.width/32):
                    self.image.blit(self.blockimage, (columns*32, rows*32))
       
    def remove_one_vert(self):
        if self.height == 32: 
            self.kill()

        else:
            self.rect.y += 32
            self.height -= 32
            self.image = pygame.Surface((self.width, self.height))
            for rows in range(0,self.height/32):
                for columns in range(0,self.width/32):
                    self.image.blit(self.blockimage, (columns*32, rows*32))
    
    def add_one_vert_bottom(self):
        self.height += 32
        self.image = pygame.Surface((self.width, self.height))
        for rows in range(0,self.height/32):
            for columns in range(0,self.width/32):
                self.image.blit(self.blockimage, (columns*32, rows*32))

    
    def add_one_vert_top(self):
        
        self.height += 32
        self.image = pygame.Surface((self.width, self.height))
        for rows in range(0,self.height/32):
            for columns in range(0,self.width/32):
                self.image.blit(self.blockimage, (columns*32, rows*32))
        
        self.rect.y -= 32
        self.pos = (self.rect.x, self.rect.y)
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip(self.pos)
        
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
        self.healthtext = Constants.healthtext.render('Health: ', 0, (255,253,255)) #load the text for the health        
        
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
        
        self.score = None
        self.scoretext = None
        self.score = 'Score: ' + str(Globals.score)
        self.scoretext = Constants.healthtext.render(self.score, 0, (255,253,255)) #load the text for the score
        self.image.blit(self.scoretext, (600, 38))


#projectile classes        

class Projectile(Entity):
    def __init__(self, x, y, xvel, yvel):
        Entity.__init__(self, Globals.group_PROJECTILES)
    
        #set the required variables    
        self.xvel = xvel
        self.yvel = yvel
        self.gravity = True
        self.numbounce = 0
        self.can_stun = False
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
                    
                
        if pygame.sprite.spritecollide(self, Globals.group_SPECIAL, False):
            self.kill()
            self.yvel = 0
        self.collidearray = pygame.sprite.spritecollide(self, Globals.group_AI, False)
        for item in self.collidearray:
            if not isinstance(self, EnemyProj):
                item.damage(self.damage)
                self.kill()
                if self.can_stun and item.can_stun: item.stun()
            
        if self.rect.x + self.rect.width < Globals.camera.xbounds[0] or self.rect.x > Globals.camera.xbounds[1] or self.rect.y < Globals.camera.ybounds[0] or self.rect.y > Globals.camera.ybounds[1]:
            self.kill()    

class Boss(Entity):
    pass

class EnemyHealthBar(Entity):
    def __init__(self, x, y, length, health, caption = None):
        Entity.__init__(self, Globals.group_DRAWONLY)
        self.health = health
        self.maxhealth = health
        self.image = pygame.Surface((length, 30))
        self.rect = pygame.Rect((x, y), (length, 100))
        self.rect.move_ip(x, y)
        self.image.fill((0,255,0))
        self.length = length
        if not caption == None:
            self.image.blit(Constants.spleentext.render(caption, 0, (0,0,0)), (10, 8)) #load the text 
            self.caption = True
            self.captiontext = caption
        else: self.caption = False    
          
    def damage(self, damage):
        self.health -= damage
        self.image.fill((255,0,0))
        if self.health > 0:
            self.percentage = float(self.health)/float(self.maxhealth)
            pygame.draw.rect(self.image, (0,255,0), pygame.Rect(0,0, self.percentage * self.length, 30))
        if self.caption: self.image.blit(Constants.spleentext.render(self.captiontext, 0, (0,0,0)), (10, 8)) #load the text 
            
class Background(pygame.sprite.Sprite):
    def __init__(self, image, loc, move_with_camera=True):
        pygame.sprite.Sprite.__init__(self, Globals.group_BG)
        self.move_with_camera = move_with_camera
        self.image = functions.get_image(image, (255,0,255))
        self.rect = self.image.get_rect()       
        self.rect.move_ip(loc) 
        self.pos = (self.rect.x, self.rect.y)

class EnemyProj(Projectile):
    pass               







#projectiles
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
        self.damage = 0
        
        if attack_left:
            Projectile.__init__(self, x, y, -7, 0)
        else:
            Projectile.__init__(self,x,y,7,0)
        self.gravity = False
        self.can_stun = True
        
    def animate(self):
        self.image = self.imagelist[self.image_index]
        if self.image_index < self.numimages: self.image_index += 1
        else: self.image_index = 0

class WikiProj(EnemyProj):
    def __init__(self, x, y, xvel, yvel):
        self.imagelist = functions.create_image_list(os.path.join('Resources','Projectiles','Bitmap','Information'), 'Information', 3, '.bmp', (255,0,255))
        self.image = self.imagelist[0]
        self.numimages = 3
        self.image_index = 0
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = x
        self.rect.y = y
        Projectile.__init__(self, x, y, xvel, yvel)
        self.damage = 2
        self.gravity = False
        
    def animate(self):
        self.image = self.imagelist[self.image_index]
        if self.image_index < self.numimages: self.image_index += 1
        else: self.image_index = 0
        

#other stuff

class Fireball(EnemyProj):
    def __init__(self, x, y, xvel, yvel, angle):
        self.imagelist = functions.create_image_list(os.path.join('Resources','Projectiles','Bitmap','TrollFlame'), 'TrollFlame', 3, '.bmp', (255,0,255))
        self.image = self.imagelist[0]
        self.numimages = 3
        self.image_index = 0
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = x
        self.rect.y = y
        Projectile.__init__(self, x, y, xvel, yvel)
        self.damage = 3
        self.gravity = False
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.numbounce = 3
    
    def animate(self):
        self.image = self.imagelist[self.image_index]
        self.image = pygame.transform.rotate(self.image, self.angle)
        if self.image_index < self.numimages: self.image_index += 1
        else: self.image_index = 0

class Coin(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, Globals.group_SPECIAL)
        self.image = functions.get_image(os.path.join('Resources', 'Stage 1 Resources', '1CoinTile.png'), (255,0,255))
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = x
        self.rect.y = y

class lazer(Entity):
    def __init__(self, x, y, left):
        Entity.__init__(self, Globals.group_PROJECTILES)
        self.collided = False
        if left: 
            self.range = -800
            self.interval = -1
        else: 
            self.range = 800
            self.interval = 1
        self.lazerimage = functions.create_image_list(os.path.join('Resources','Projectiles','Lazer fragments'), 'frag_', 5, '.bmp', (255,0,255))
        for i in range(0, self.range, self.interval):
            self.rect = pygame.Rect(x + i, y, 1, 11)
            if pygame.sprite.spritecollide(self, Globals.group_COLLIDEBLOCKS, False) or pygame.sprite.spritecollide(self, Globals.group_SPECIAL, False) or self.rect.x == 0 or self.rect.x == Globals.camera.xbounds[1]:
                self.range = i
                break
            
        self.image = pygame.Surface((abs(self.range), 11))
        if left:
            for i in range(0, self.range, self.interval):
                if i == self.range + 1: self.image.blit(self.lazerimage[0], (abs(i), 0))
                elif i == self.range + 2: self.image.blit(self.lazerimage[1], (abs(i), 0))
                elif i == self.range + 3: self.image.blit(self.lazerimage[2], (abs(i), 0))
                elif i == self.range + 4: self.image.blit(self.lazerimage[3], (abs(i), 0))
                else: self.image.blit(self.lazerimage[5], (abs(i), 0))
        else: 
            for i in range(0, self.range, self.interval):
                if abs(i) == 0: self.image.blit(self.lazerimage[0], (abs(i), 0))
                elif abs(i) == 1: self.image.blit(self.lazerimage[1], (abs(i), 0))
                elif abs(i) == 2: self.image.blit(self.lazerimage[2], (abs(i), 0))
                elif abs(i) == 3: self.image.blit(self.lazerimage[3], (abs(i), 0))
                else: self.image.blit(self.lazerimage[5], (abs(i), 0))
            

        self.rect = self.image.get_rect()
        if left: self.rect.move_ip(x + self.range,y)
        else: self.rect.move_ip(x,y)
        self.damage = 10
        self.duration = 30
        self.time = 1
        
    def update(self):
        if self.time%self.duration == 0: self.kill()
        else: self.time += 1
        collide = pygame.sprite.spritecollide(self, Globals.group_AI, False)
        for item in collide:
            item.damage(10)
             
                   
#Text classes
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


#stage 1
class Troll(Entity):
    def __init__(self, x, y, facingL, (leftpatrollimit, rightpatrollimit), (chasex, chasey, chasewidth, chaseheight)):
        Entity.__init__(self, Globals.group_AI)
        #load images
        self.imageloc = os.path.join('Resources','Stage 1 Resources','Troll','Bitmaps')
        self.imagepaths = {   'walkL':(os.path.join(self.imageloc,'TrollWalkL'), 'TrollWalkL', 3),
                              'walkR':(os.path.join(self.imageloc,'TrollWalkR'), 'TrollWalkR', 3),
                              'idleL':(os.path.join(self.imageloc,'TrollstandL'), 'TrollStandL', 0),
                              'idleR':(os.path.join(self.imageloc,'TrollStandR'), 'TrollStandR', 0),
                              'explodeL':(os.path.join(self.imageloc,'TrollExplodeL'), 'TrollExplodeL', 5),
                              'explodeR':(os.path.join(self.imageloc,'TrollExplodeR'), 'TrollExplodeR', 5)
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
        self.xvel = 0.0
        self.yvel = 0.0
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip((x,y))
        self.health = 3
        self.pausecycles = 1
        self.can_damage = True
        self.x = self.rect.x
        self.y = self.rect.y
        self.stunned = False
        self.detected = False
        self.status = 'patrol'
        self.distance = 0
        self.patrollimits = (leftpatrollimit, rightpatrollimit)
        self.can_die = True
        self.can_stun = True        
        self.damage_on_contact = False
        self.chaserect = pygame.Rect(chasex, chasey, chasewidth, chaseheight)
        
        
    def animate(self):
        self.image = self.images[self.imagename][self.image_index]
        if self.image_index < self.numimages: 
            self.image_index += 1
        else: 
            if self.imagename == 'explodeL' or self.imagename == 'explodeR':
                self.kill()
            else:
                self.image_index = 0
    
    def update(self):
        print self.status
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip((self.x, self.y))
        self.event()
        self.rect.x += self.xvel
        block_hit_list = pygame.sprite.spritecollide(self, Globals.group_COLLIDEBLOCKS, False) #create a list full of all blocks that troll is colliding with
        for block in block_hit_list: #iterate through the list
            #Collision moving right means that troll collided with left side of block
            if self.xvel > 0:
                self.rect.right = block.rect.left #set right side to left side of block
            elif self.xvel < 0:
                #Collision moving left means player collided with right side of block
                self.rect.left = block.rect.right #set left side to right side of block
           
        #apply gravity
        if self.yvel < 10:
            self.yvel += abs(self.yvel) / 40 + 0.36
        #move y and check for collisions
        self.rect.y += self.yvel
        block_hit_list = pygame.sprite.spritecollide(self, Globals.group_COLLIDEBLOCKS, False) #create list of blocks that troll is colliding with  
        for block in block_hit_list: #iterate over list
            # check collision
            if self.yvel > 0: #top collision
                self.rect.bottom = block.rect.top #set bottom to top of block
                self.yvel = 0 #stop vertical movement
            elif self.yvel < 0: #bottom collision
                self.rect.top = block.rect.bottom  #set top to the bottom of block
                self.yvel = 0 #stop vertical movement

        if self.rect.y + self.rect.height <= Globals.camera.ybounds[0] or self.rect.y >= Globals.camera.ybounds[1] or self.rect.x + self.rect.width <= Globals.camera.xbounds[0] or self.rect.x >= Globals.camera.xbounds[1]:
            self.kill()
        
        if not self.status == 'runl' and not self.status == 'runr' and not self.status == 'explode' and self.chaserect.collidepoint((Globals.player.x, Globals.player.y)):
            if self.facingL and Globals.player.rect.x < self.rect.x: self.status = 'detected'
            elif not self.facingL and Globals.player.rect.x > self.rect.x: self.status = 'detected'
        #animations
        if self.facingL and not self.status == 'explode':
            if self.xvel == 0:
                if not self.imagename == 'idleL':
                    self.change_image('idleL')
            else:
                if not self.imagename == 'walkL':
                    self.change_image('walkL')
        elif not self.facingL and not self.status == 'explode':
            if self.xvel == 0:
                if not self.imagename == 'idleR':
                    self.change_image('idleR')
            else:
                if not self.imagename == 'walkR':
                    self.change_image('walkR')
        
                
        self.x = self.rect.x
        self.y = self.rect.y        

    def event(self): 
        if self.status == 'patrol':
            if self.facingL:
                self.xvel = -2
                if self.rect.x < self.patrollimits[0]:
                    self.status = 'stopL'
                    self.xvel = 0
            if not self.facingL:
                self.xvel = 2
                if self.rect.x + self.rect.width > self.patrollimits[1]:
                    self.status = 'stopR'
                    self.xvel = 0
        elif self.status == 'stopL':
            if self.pausecycles%180 == 0:
                self.pausecycles = 1
                self.status = 'patrol'
                self.facingL = False
            else: self.pausecycles += 1
            
        elif self.status == 'stopR':
            if self.pausecycles%180 == 0:
                self.pausecycles = 1
                self.status = 'patrol'
                self.facingL = True
            else: self.pausecycles += 1  
        elif self.status == 'detected':
            if Globals.player.rect.x > self.rect.x: 
                self.status = 'runr'
                self.rect.x += 5
            elif Globals.player.rect.x < self.rect.x: 
                self.status = 'runl'
                self.rect.x -= 5
        elif self.status == 'runr':
            print 'running'
            if self.rect.x + self.rect.width < self.patrollimits[1]: self.xvel = 4       
            else: self.damage(100)
        elif self.status == 'runl':
            if self.rect.x > self.patrollimits[0]: self.xvel = -4
            else: self.damage(100)
        
        
    def damage(self, damage):
        self.health -= damage
        if self.health <= 0 and self.can_die:
            self.can_die = False
            self.health = 0
            self.status = 'explode'
            self.xvel = 0
            if self.facingL:
                if not self.imagename == 'explodeL': 
                    self.change_image('explodeL')
                    self.rect.x -= 4
                    self.x -= 4
                    self.rect.y -= 16
                    
            else:
                if not self.imagename == 'explodeR': 
                    self.change_image('explodeR')
                    self.x -= 18
                    self.rect.x -= 18
                    self.rect.y -= 16
                   
    def change_image(self, image):
        
        if not self.imagename == image:
            self.image_index = 0 #reset the image position
            self.imagename = image #change the image list
            self.image = self.images[self.imagename][0] #set the image to the first image in the list
            self.numimages = len(self.images[self.imagename]) - 1 #set the length of the list
                    
    def stun(self):
        self.currentevent = 'stunned'
        self.xvel = 0
        self.can_stun = False

class Wikipedia(Entity):
    def __init__(self, x, y, patroldist):
        Entity.__init__(self, Globals.group_AI)
        self.image = functions.get_image(os.path.join('Resources','Stage 1 Resources','Wikipedia','Wikipedia.bmp'), (255,0,255))
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = x
        self.rect.y = y
        self.patroldist = patroldist
        self.currentevent = 'patroldown'
        self.patrolspeed = 1
        self.patrolled = 0
        self.xvel = 0
        self.yvel = 0
        self.stuntimer = 80
        self.stuncounter = 0
        self.down = True
        self.can_stun = True
        self.health = 5
        self.can_damage = True
        self.damage_on_contact = True
    
    def damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def update(self):
        self.event()
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        
    def animate(self):
        pass 
    
    def event(self):
        if self.currentevent == 'patroldown':
            if self.patrolled >= self.patroldist:
                self.currentevent = 'patrolup'
                self.patrolled = 0
                self.shoot(False)
                self.down = False
                
            else:
                self.yvel = self.patrolspeed
                self.patrolled += self.patrolspeed
        
        elif self.currentevent == 'patrolup':
            if self.patrolled >= self.patroldist:
                self.currentevent = 'patroldown'
                self.patrolled = 0
                self.shoot(True)
                self.down = True
                
            else:
                self.yvel = -self.patrolspeed
                self.patrolled += self.patrolspeed
                
        elif self.currentevent == 'stunned':
            if self.stuncounter == self.stuntimer:
                self.stuncounter = 0
                self.patrolspeed = 1
                self.can_stun = True
                if self.down: self.currentevent = 'patroldown'
                else: self.currentevent = 'patrolup'
            else: self.stuncounter += 1
    def shoot(self, up):
        if up:
            proj1 = WikiProj(self.rect.x - 32, self.rect.y, -4, 0)
            proj2 = WikiProj(self.rect.x + self.rect.width, self.rect.y, 4, 0)
        else:
            proj1 = WikiProj(self.rect.x - 32, self.rect.y + self.rect.height - 32, -4, 0)
            proj2 = WikiProj(self.rect.x + self.rect.width, self.rect.y + self.rect.height - 32, 4, 0)
    
    def stun(self):
        self.currentevent = 'stunned'
        self.can_stun = False
        self.xvel = 0
        self.yvel = 0
        self.patrolspeed = 0
        print 'Stunned'
                
class InternetBoss(Boss):
    def __init__(self, x, y):
        Entity.__init__(self, Globals.group_AI)
        
        #load images
        self.imageloc = os.path.join('Resources','Stage 1 Resources','Boss','Bitmaps')
        self.imagepaths = {   'dashL':(os.path.join(self.imageloc,'DashL'), 'Bossdash', 3),
                              'dashR':(os.path.join(self.imageloc,'DashR'), 'BossdashR', 3),
                              'idleL':(os.path.join(self.imageloc,'IdlingL'), 'idleL', 5),
                              'idleR':(os.path.join(self.imageloc,'IdlingR'), 'idleR', 5),
                              'spit':(os.path.join(self.imageloc,'Spit'), 'SpitL', 15),
                              'die':(os.path.join(self.imageloc,'Die'), 'Bossdie', 29),
                              'smash':(os.path.join(self.imageloc,'Smash'), 'BossSmash', 11),
                              'shout':(os.path.join(self.imageloc,'Shout'), 'BossShout', 15),
                              'lift':(os.path.join(self.imageloc,'Lift'), 'Bosslift', 2),
                              'hold':(os.path.join(self.imageloc, 'BossDoorWait'),'BossDoorWait', 9)                              
   
                          }
        self.images = {}
        self.images = functions.load_imageset(self.imagepaths) #populates self.images with a dictionary of the above images with format 'imagename':image
                
        #set the current image to the loaded one
        self.imageindex = 0
        self.imagename = 'idleL'
        self.image = self.images[self.imagename][0]
        self.numimages = len(self.images[self.imagename]) - 1
        
        #collision box
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip((x, y))
        
        #other variables
        self.can_stun = True
        self.currentevent = 'pause_intro'
        self.can_damage = True
        self.health = 40
        self.damage_on_contact = True
        self.xvel = 0.0
        self.yvel = 0.0
        self.facingL = True
        self.pausetimer = 120
        self.pausecounter = 0
        self.x = x
        self.y = y
        self.blockcounter = 20
        self.blocktimer = 0
        self.healthbar = EnemyHealthBar(30,15, 680, self.health, 'BOSS HEALTH: ')
        self.first_blocks = False
        self.numcycles = 0
        self.touchingwalls = False
        self.intro = True
        
        Globals.player.arrowkey_enabled = False
        Globals.player.can_attack = False
   
    def update(self):
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.move_ip((self.x, self.y))
        self.touchingwalls = False
        
        self.rect.x += self.xvel
        block_hit_list = pygame.sprite.spritecollide(self, Globals.group_COLLIDEBLOCKS, False) #create a list full of all blocks that troll is colliding with
        for block in block_hit_list: #iterate through the list
            #Collision moving right means that troll collided with left side of block
            if self.xvel > 0:
                self.rect.right = block.rect.left #set right side to left side of block
                self.touchingwalls = True
            elif self.xvel < 0:
                #Collision moving left means player collided with right side of block
                self.rect.left = block.rect.right #set left side to right side of block
                self.touchingwalls = True
        
        self.event()
        #animations
        if not self.intro:
            if self.facingL and not self.currentevent == 'die' and not self.currentevent == 'spit':
                if self.xvel == 0:
                    if not self.imagename == 'idleL':
                        self.change_image('idleL')
                else:
                    if not self.imagename == 'dashL':
                        self.change_image('dashL')
            elif not self.facingL and not self.currentevent == 'die' and not self.currentevent == 'spit':
                if self.xvel == 0:
                    if not self.imagename == 'idleR':
                        self.change_image('idleR')
                else:
                    if not self.imagename == 'dashR':
                        self.change_image('dashR')
        
                
        self.x = self.rect.x
        self.y = self.rect.y        
    
    def event(self):
        if self.currentevent == 'pause_intro':
            if self.pausecounter == self.pausetimer:
                self.pausecounter = 0
                self.change_image('smash')
            else: self.pausecounter += 1
            
        elif self.currentevent == 'create_stage':
            if self.blocktimer == self.blockcounter:
                self.blocktimer = 0
                if self.first_blocks:
                    if self.numcycles < 9:
                        self.door1.add_one_vert_top()
                        self.door2.add_one_vert_top()
                        self.numcycles += 1
                    else: 
                        self.currentevent = 'roar'
                        self.change_image('lift')
                else: 
                    self.first_blocks = True
                    self.door1 = Door(0*32, 11*32,1,1, 1)
                    self.door2 = Door(24*32, 11*32,1,1, 1)

            else: self.blocktimer += 1
        
        elif self.currentevent == 'intropause':
            if self.pausetimer % self.pausecounter == 0:
                self.currentevent ='determine_attack'
                Globals.player.arrowkey_enabled = True
                Globals.player.can_attack = True
                self.intro = False
                self.pausecounter = 0
            else:self.pausecounter += 1
        
        elif self.currentevent == 'dashL':
            self.facingL = True
            if self.rect.colliderect(Globals.player.rect):
                self.currentevent = 'pausing'
                self.pausetimer = 60
                self.xvel = 0
                self.facingL = False
                self.damage_player(4, 'left')

            else:
                if self.touchingwalls:
                    self.currentevent = 'pausing'
                    self.pausetimer = 120
                    self.xvel = 0
                    self.facingL = False
                
                else:
                    self.xvel = -7
        elif self.currentevent == 'dashR':
            self.facingL = False
            if self.touchingwalls:
                self.currentevent = 'pausing'
                self.pausetimer = 120
                self.xvel = 0
                self.facingL = True
                
            else:
                self.xvel = 7
        
        elif self.currentevent == 'pausing':
            if self.pausecounter == self.pausetimer:
                self.pausecounter = 0
                if not self.facingL: self.currentevent = 'dashR'
                else: self.currentevent = 'determine_attack'
            else: 
                self.pausecounter += 1
        
        elif self.currentevent == 'stun':
            if self.pausecounter == self.pausetimer:
                self.pausecounter = 0
                if self.facingL: self.currentevent = 'dashR'
                else: self.currentevent = 'determine_attack'
            else: 
                self.pausecounter += 1
        
        elif self.currentevent == 'determine_attack':
            self.randnum = randrange(1, 12, 1)
            if self.randnum >= 6: self.currentevent = 'dashL'
            else: self.currentevent = 'spit'
            
        elif self.currentevent == 'spit':
            if not self.imagename == 'spit': self.change_image('spit')
        
    def stun(self):
        if self.currentevent == 'dashL':
            self.currentevent = 'stun'
            self.pausetimer = 120
            self.xvel = 0
      
    def damage(self, damage):
        self.health -= damage
        self.healthbar.damage(damage)
        if self.health <= 0 and not self.currentevent == 'die':
            self.currentevent = 'die'
            self.change_image('die')
            self.xvel = 0
            Globals.player.arrowkey_enabled = False
            Globals.player.can_attack = False
            Globals.player.xvel = 0
                    
    def damage_player(self, damage, pushdirection):
        if pushdirection == 'left':
            Globals.player.xvel = -13
            Globals.player.yvel = -14
            Globals.player.health -= damage
            Globals.player.lock_midair = True
        elif pushdirection == 'right':
            Globals.player.xvel = 15
            Globals.player.yvel = -20
            Globals.player.health -= damage
            Globals.player.lock_midair = True
                    
    def animate(self):
        self.image = self.images[self.imagename][self.imageindex]
        if self.imageindex < self.numimages: 
            self.imageindex += 1
            if self.imagename == 'spit' and self.imageindex == 13:
                self.fireball()
            
        else: 
            if self.imagename == 'die':
                goal = goal_piece(self.rect.center[0], self.rect.center[1])
                Globals.player.arrowkey_enabled = True
                Globals.player.can_attack = True
                self.healthbar.kill()
                self.kill()
            
            elif self.imagename == 'smash': 
                self.currentevent = 'create_stage'
                self.change_image('hold')
            
            elif self.imagename == 'lift':
                self.currentevent = 'roar'
                self.change_image('shout')
            
            elif self.imagename == 'shout':
                self.currentevent = 'intropause'
                self.change_image('idleL')
                
            elif self.imagename == 'spit':
                self.currentevent = 'pausing'
                self.change_image('idleL')
                
            else:
                self.imageindex = 0
        
    def change_image(self, image):
        self.imageindex = 0 #reset the image position
        self.imagename = image #change the image list
        self.image = self.images[self.imagename][0] #set the image to the first image in the list
        self.numimages = len(self.images[self.imagename]) - 1 #set the length of the list
        
    def fireball(self):
        self.xpos = self.rect.x + 33
        self.ypos = self.rect.y + self.rect.height/3 + 18
        self.playerx = (Globals.player.rect.x + Globals.player.rect.width/2) - self.xpos
        self.playery = (Globals.player.rect.y + 19) - self.ypos
        angle_to_player = math.atan2(self.playery,self.playerx)
        self.projxvel = 19*math.cos(angle_to_player)
        self.projyvel = 19*math.sin(angle_to_player)
        dis_to_player = math.sqrt((self.playerx)**2 + (self.playery)**2)
        fireball = Fireball(self.xpos, self.ypos, self.projxvel, self.projyvel, 850*angle_to_player/dis_to_player)
        
#Buttons       
class Menu_PlayButt(Button):
    def __init__(self, x, y):
        self.image = functions.get_image(os.path.join('Resources','General Resources','Buttons','PlayButt.bmp'), (255,0,255))
        Button.__init__(self, x, y)
        
    def clicked(self):
        print "Play button clicked"
        
class Menu_InfoButt(Button):
    def __init__(self, x, y):
        self.image = functions.get_image(os.path.join('Resources','General Resources','Buttons','InfoButt.bmp'), (255,0,255))
        Button.__init__(self, x, y)
        
    def clicked(self):
        print "info button clicked"

class Menu_ScoresButt(Button):
    def __init__(self, x, y):
        self.image = functions.get_image(os.path.join('Resources','General Resources','Buttons','ScoresButt.bmp'), (255,0,255))
        Button.__init__(self, x, y)
        
    def clicked(self):
        print "Scores button clicked"
        
class Menu_QuitButt(Button):
    def __init__(self, x, y):
        self.image = functions.get_image(os.path.join('Resources','General Resources','Buttons','QuitButt.bmp'), (255,0,255))
        Button.__init__(self, x, y)
        
    def clicked(self):
        print "Quit button clicked"
