#! /usr/bin/env python

"""
utility functions
"""

import os
import pygame
from pygame.locals import *

def loadImage(directory, imgName, colorkey=None):
    fullname = os.path.join(directory, imgName)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def printGroceryList(self, recipeList):
    groceryList = GroceryList(recipeList)

    for item in groceryList.getList():
        print item.toString()
