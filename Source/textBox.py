#! /usr/bin/env/ python

import pygame
from pygame.locals import *
from pygame import sprite

from utils import loadImage
from pygame.sprite import Sprite
from pygame.sprite import Group

from ingredient import Ingredient

from button import Button
from textBlock import TextBlock

import os
    
    
## this is just a frame for me to put a TextBlock inside of for copy and pasting, and for typing
class TextBox(Sprite):
    def __init__(self, ID, wh, loc, font, imgFolder):
        Sprite.__init__(self)
        self.theFont = font
        self.width, self.height = wh
        self.identity = ID
        self.text = "++++"

        self.image = pygame.Surface(wh)
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()

        self.doneButton = Button(imgFolder, "textButton", (self.rect.left, self.rect.bottom - 166),
                                 "done", -1)
        self.doneButton.addText("Add Entry")
    
        self.image.blit(self.doneButton.getImage(), self.doneButton.getRect())

        x,y = loc
        self.rect.top += y
        self.rect.left += x

    def setLocation(self, loc):
        x,y = loc
        self.rect.top += y
        self.rect.left += x

    def getIdentity(self):
        return self.identity

    def isClicked(self, xy):
        # need to scale the xy value to be relative to the textBox window
        x,y = xy
        x -= self.rect.left
        y -= self.rect.top
        xy = x,y
        
        if self.doneButton.getRect().collidepoint(xy):
             return self.text
        else:
            return None
        

    def addText(self, string):
        self.text = string
        textBox = TextBlock("doesntMatter", string, self.theFont, 15,60, self.height - 200)
        self.image.blit(textBox.getImage(), textBox.getRect())

    def getRect(self):
        return self.rect

    def getImage(self):
        return self.image

    def scroll(self, dy):
        pass




    
            
