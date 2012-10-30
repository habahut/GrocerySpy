#! /usr/bin/env/ python


import pygame
from pygame.locals import *
from pygame import sprite

from utils import loadImage
from pygame.sprite import Sprite
from pygame.sprite import Group


class Button(Sprite):

    def __init__(self, imgFolder, mode, loc, ident, colorKey = None):
        pygame.sprite.Sprite.__init__(self)

        self.identity = ident

        ## might have been smarter to just make the mode == fileName
        # that way instead of an if statement could just have
        # load "mode.<ext>"
        if mode == "textButton": ## red Box
            self.image, self.rect = loadImage(imgFolder, "redButton.png", colorKey)
        elif mode == "expandButton": ## horizontal expandButton
            self.image,self.rect = loadImage(imgFolder, "arrow_buttonHorizontal.gif", colorKey)
        elif mode == "unExpandButton": ## vertical expandButton
            self.image,self.rect = loadImage(imgFolder, "arrow_buttonVertical.gif", colorKey)
        elif mode == "addToGroceryListButton": ## shopping cart button
            self.image,self.rect = loadImage(imgFolder, "shoppingCart.png", colorKey)
        elif mode == "removeFromGroceryListButton": ##
            self.image,self.rect = loadImage(imgFolder, "shoppingCartAdded.png", colorKey)
        elif mode == "backButton":
            self.image,self.rect = loadImage(imgFolder, "backButton.png", colorKey)
        elif mode == "checkBox":
            self.image,self.rect = loadImage(imgFolder, "checkBox.png", colorKey)
        elif mode =="writeToDesktop":
            self.image,self.rect = loadImage(imgFolder, "writeToDesktop.jpg", colorKey)
        elif mode == "delete":
            self.image,self.rect = loadImage(imgFolder, "deleteButton.png", colorKey)
        elif mode == "deleted":
            self.image,self.rect = loadImage(imgFolder, "isDeletedButton.png", colorKey)
            
            
        self.rect.topleft = loc
        self.active = True

    def addText(self, string, col=(255,255,255)):
        if not pygame.font.get_init():
            pygame.font.init()
        #theFont = pygame.font.Font(None, 30)
        theFont = pygame.font.Font("freesansbold.ttf", 15)
        text = theFont.render(string, False, col)
        
        ## the position is relative to the coordinates on the IMAGE, not
        # the screen. So the top left of this image is at (0,0) for this
        # function, not (x,y) where x and y represent screen coordinates
        self.image.blit(text,
                        (self.image.get_width()/2 - text.get_width() /2,
                         self.image.get_height()/2 - text.get_height() /2))
        
        self.image.convert()
        
    def getRect(self):
        return self.rect

    def getIdentity(self):
        return self.identity

    def getImage(self):
        return self.image

    def updateY(self, dy):
        self.rect.top += dy

    def __str__(self):
        return "button @ "+ self.rect.__str__()+ " ID: "+ self.identity
