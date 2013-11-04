'''
Created on 31/10/2013

@author: 22491
'''
import pygame, os, sys, Entities, functions, Constants

def level_1():
    level_layout = ("W                               W",
                    "W                               W",
                    "W                               W",
                    "W                               W",
                    "W                               W",
                    "W                               W",
                    "W                               W",
                    "W                               W",
                    "W                               W",
                    "W                               W",
                    "W                               W",
                    "W                               W",
                    "W                               W",
                    "W           S                   W",
                    "W M                             W",
                    "W                               W",
                    "FFFFFFFFFFFFFFFFFF      FFFFFFFFF",
                    "                                 ",
                    "                                 ",
                    "                                 ",
                    "                                 "                  
                    )
    blocklayout = functions.returnlayoutlist(level_layout)
    return blocklayout