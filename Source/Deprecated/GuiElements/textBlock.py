#! /usr/bin/env/ python

import pygame
from pygame.locals import *
from pygame import sprite

from utils import loadImage
from pygame.sprite import Sprite
from pygame.sprite import Group

class TextBlock(Sprite):
    def __init__(self, name, stringData, font, locY, maxHeight = 100000):
        pygame.sprite.Sprite.__init__(self)
        self.location = locY
        self.theFont = font

        self.name = name

        self.addText(stringData)

    def addText(self, stringData, maxHeight = 100000):
        allLines = stringData.split("\n")
        
        allTextImages = []
        totalHeight = 0
        widestWidth = 0

        print allLines

        if isinstance(allLines, str):
            print allLines, " was a string"
            listWrapper = allLines
            allLines = []
            allLines.add(listWrapper)
        
        for line in allLines:
            #print "RENDERING LINE: ", line
            thisLineImage = self.theFont.render(line, False, (255,255,255))            
            totalHeight += thisLineImage.get_height()
            if (totalHeight > maxHeight):
                totalHeight -= thisLineImage.get_height()
                print "     size overflow"
                break
            allTextImages.append(thisLineImage)
            if thisLineImage.get_width() > widestWidth:
                widestWidth = thisLineImage.get_width()
                
        totalHeight += 7
        widestWidth += 50
        self.image = pygame.Surface((widestWidth, totalHeight))
        textBlockCursor = 5
        
        for imageLine in allTextImages:
            self.image.blit(imageLine, (5, textBlockCursor ))
            textBlockCursor += imageLine.get_height()

        self.image.convert()
        
        self.rect = self.image.get_rect()
        x,y = self.rect.topleft
        y += self.location
        self.rect.topleft = x,y

    def get_height(self):
        return self.image.get_height()

    def getName(self):
        return self.name

    def getLeftBorder(self):
        return 55

    def getImage(self):
        return self.image

    def getRect(self):
        return self.rect

    def getBlitPos(self):
        x,y = self.rect.topleft
        x += self.getLeftBorder()
        return x,y

    def updateY(self, dy):
        self.rect.top += dy        

    def collideButtons(self, xy):
        ## even if they did click on the text box, we don't want to do
        # anything to it so we just return None
        return None

    def __str__(self):
        return "row: "+ self.name+ "  @ "+ self.rect.__str__()

    

