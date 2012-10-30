#! /usr/bin/env/ python

import pygame
from pygame.locals import *
from pygame import sprite

from utils import loadImage
from pygame.sprite import Sprite
from pygame.sprite import Group



# the goal is to make this more general, so that it can store a recipe or a grocery item
# so we can display recipes when we want to browse all recipes,
# and when compiling a grocery list we can also then pass that into the scrollable window constructor
# and make a grocery list thing as well...
class Row(Sprite):

    def __init__(self, objectName, font, locY, imgdir, mode, ing = None):
        pygame.sprite.Sprite.__init__(self)

        col = 255,255,255

        self.locationY = locY
        self.name = objectName
        self.theFont = font
        self.imgFolder = imgdir

        self.nameText = self.theFont.render(self.name, False, col)
        self.image = pygame.Surface((700, self.nameText.get_height() + 2))

        # this stores the ingredient if we are in "groceryListViewer" mode
        # should not be used by recipeViewer, but we store it here anyway so python doesn't complain
        # this will be useful later for scaling the amount stored
        self.ingredient = ing
        
        if mode == "recipeViewer":            
            ## in this mode, we need the buttons to expand recipes and add them to the shopping cart
            self.expandButton = Button(self.imgFolder, "expandButton", (10, 0), "expand@"+self.name, -1)
            self.image.blit(self.expandButton.getImage(), self.expandButton.getRect())
            
            
            self.groceryListButton = Button(self.imgFolder, "addToGroceryListButton",
                                        (self.nameText.get_width() + self.expandButton.getImage().get_width() + 25, 0),
                                        "addToGroceryList@"+self.name, -1)
            self.image.blit(self.groceryListButton.getImage(), self.groceryListButton.getRect())

            ## we put the name text in a different spot if we have the expand button
            self.image.blit(self.nameText, (self.expandButton.getImage().get_width() + 15, 0))

            self.allButtons = [self.expandButton, self.groceryListButton]
        elif mode == "groceryListViewer":
            self.image.blit(self.nameText, (15, 0))
            ## put remove item and scale quantity boxes in here...
      
        self.image.convert()

        self.rect = self.image.get_rect()
        x,y = self.rect.topleft
        y += locY
        self.rect.topleft = x,y

    def toggleButton(self, buttonType):
        ## need to toggle the add to groceryList buttons!!!        
        if buttonType == "expand":
            #pygame.draw.rect(self.image, (0,0,0), self.expandButton.getRect(), 0)
            buttonIDs = self.expandButton.getIdentity().split("@")
            self.allButtons.remove(self.expandButton)
            self.expandButton = Button(self.imgFolder, "unExpandButton",
                                       (self.expandButton.getRect().topleft), "unExpand@"+buttonIDs[1], -1)
            self.allButtons.append(self.expandButton)
            self.image.blit(self.expandButton.getImage(), self.expandButton.getRect())
            
        elif buttonType == "unExpand":
            buttonIDs = self.expandButton.getIdentity().split("@")
            self.allButtons.remove(self.expandButton)
            self.expandButton = Button(self.imgFolder, "expandButton",
                                       (self.expandButton.getRect().topleft), "expand@"+buttonIDs[1], -1)
            self.allButtons.append(self.expandButton)
            self.image.blit(self.expandButton.getImage(), self.expandButton.getRect())

        elif buttonType == "groceryButton":
            #pygame.draw.rect(self.image, (0,255,0), self.groceryListButton.getRect(), 0)
            self.allButtons.remove(self.groceryListButton)
            
            buttonIDs = self.groceryListButton.getIdentity().split("@")
            if buttonIDs[0] == "addToGroceryList":                
                self.groceryListButton = Button(self.imgFolder, "removeFromGroceryListButton",
                                                (self.groceryListButton.getRect().topleft),
                                                "removeFromGroceryList@"+buttonIDs[1],-1)                               
            else:
                self.groceryListButton = Button(self.imgFolder, "addToGroceryListButton",
                                                (self.groceryListButton.getRect().topleft),
                                                "addToGroceryList@"+buttonIDs[1],-1) 
            self.image.blit(self.groceryListButton.getImage(), self.groceryListButton.getRect().topleft)
            self.allButtons.append(self.groceryListButton)
        
    def isAddedToGroceryList(self):
        buttonIDs = self.groceryListButton.getIdentity().split("@")
        if buttonIDs[0] == "addToGroceryList":
            return False
        else:
            return True

    def getImage(self):
        return self.image

    def getRect(self):
        return self.rect

    def getBlitPos(self):
        x,y = self.rect.topleft
        x += self.getLeftBorder()
        return x,y

    def getName(self):
        return self.name

    def get_height(self):
        return self.image.get_height()

    def getLeftBorder(self):
        return 0

    def updateY(self, dy):
        self.rect = self.rect.move(0, dy)        
        
    def collideButtons(self, xy):
        # need to convert the xy location of the mouse click to be relative to the top left of the row
        x,y = xy
        y-= self.rect.top
        xy = x,y
        for button in self.allButtons:
            if button.getRect().collidepoint(xy):
                return button
        return None

    ## this method is only for groceryListViewer
    # all scaling done to the ingredient list will be stored in this rows "ingredient" object
    # we then return the object for printing to file or for storing the groceryList
    def getModifiedIngredient(self):
        print "returning : ", self.ingredient
        return self.ingredient

