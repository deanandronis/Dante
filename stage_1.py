'''
Created on 31/10/2013

@author: Dean, God Almighty of Sex and Women
'''
import pygame, os, sys, Entities, functions, Constants, Globals

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
                    "W M                           G W",
                    "W                               W",
                    "FFFFFFFFFFFFFFFFFF      FFFFFFFFF",
                    "                                 ",
                    "                                 ",
                    "                                 ",
                    "                                 "                  
                    )
    blocklayout = functions.returnlayoutlist(level_layout, 1)
    return blocklayout

def level_2():
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
                    "W M                           G W",
                    "W                               W",
                    "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
                    "                                 ",
                    "                                 ",
                    "                                 ",
                    "                                 "                  
                    )
    blocklayout = functions.returnlayoutlist(level_layout, 1)
    return blocklayout