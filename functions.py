'''
Created on Oct 27, 2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, sys, os, math
from pygame.locals import *
import Entities, Constants

def get_image(path, colorkey):
    image = pygame.image.load(path).convert()
    image.set_colorkey(colorkey)
    return image

def create_image_list(path, filename, numimages, filetype,colorkey):
    imagelist = []
    if numimages >= 10:
        for i in range(0,numimages+1):
            if i < 10:
                imageloc = os.path.join(path, filename) +'0' + str(i) + filetype
                image = get_image(imageloc,colorkey)
                imagelist.append(image)
                
            else:
                imageloc = os.path.join(path, filename) + str(i) + filetype
                image = get_image(imageloc, colorkey)
                imagelist.append(image)
    else:
        for i in range(0,numimages + 1):
            imageloc = os.path.join(path,filename) + str(i) + filetype
            image = get_image(imageloc,colorkey)
            imagelist.append(image)
            
    return imagelist

def load_imageset(imagedict):
    images = {}
    for item in imagedict.keys():
            images[item] = create_image_list(imagedict[item][0], imagedict[item][1], imagedict[item][2], '.bmp', (255,0,255))
    return images

def xfrange(start, stop, step):
    while start < stop:
        yield start
        start += step
