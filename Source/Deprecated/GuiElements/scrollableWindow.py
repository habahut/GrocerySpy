#! /usr/bin/env/ python

import pygame
from pygame.locals import *
from pygame import sprite

from utils import loadImage
from pygame.sprite import Sprite
from pygame.sprite import Group


class ScrollableWindow(Sprite):

    INITIAL_CURSOR_POS = 20
    CURSOR_BORDER_INCREMENT = 20

    def __init__(self, imgdir, wh, screenSize, mode):
        pygame.sprite.Sprite.__init__(self)

        self.windowWidth, self.windowHeight = screenSize

        self.rect = pygame.Rect((0,0), wh)

        self.image = pygame.Surface(wh)
        self.imageMaxY, self.imageMaxX = wh

        # the initial position of the cursor...
        self.cursorY = self.INITIAL_CURSOR_POS

        # a list of all the text that has been put on this window
        # we will need this later for removing stuff        
        self.allElements = []

        # the location of the camera, calling scroll will change this
        self.cameraY = 0        

        self.imgFolder = imgdir

        self.mode = mode

        if not pygame.font.get_init():
            pygame.font.init()
        self.theFont = pygame.font.Font(None, 30)

    def addText(self, stringList, col=(255,255,255)):
        if isinstance(stringList, str):
            temp = stringList
            stringList = []
            stringList.append(temp)
        
        for string in stringList:
            thisRow = Row(string, self.theFont, self.cursorY, self.imgFolder, self.mode)
            rowImage = thisRow.getImage()
            self.allElements.append(thisRow)
        
            self.checkResize(self.cursorY + rowImage.get_height())
            self.image.blit(rowImage, (0, self.cursorY))
            self.cursorY += rowImage.get_height() + self.CURSOR_BORDER_INCREMENT

    def addGroceryList(self, groceryList, col=(255,255,255)):
        if isinstance(groceryList, Ingredient):
            temp = groceryList
            groceryList = []
            groceryList.append(temp)

        for ingredient in groceryList:
            thisRow = Row(ingredient.getFullName(),
                          self.theFont, self.cursorY, self.imgFolder, self.mode, ingredient)
            rowImage = thisRow.getImage()
            self.allElements.append(thisRow)
        
            self.checkResize(self.cursorY + rowImage.get_height())
            self.image.blit(rowImage, (0, self.cursorY))
            self.cursorY += rowImage.get_height() + self.CURSOR_BORDER_INCREMENT

    def redrawAll(self):
        self.redrawUpToNum(len(self.allElements))

    def redrawUpToLE(self, lastElement):   
        for i, sprite in enumerate(self.allElements):
            if sprite == lastElement:
                break;

        if i > len(self.allElements):
            print "ERROR HERE, element passed not in sprites"
        else:
            redrawUpToNum(i)
        

    def redrawUpToNum(self, num):
        self.image.fill((0,0,0))
        self.cursorY = self.INITIAL_CURSOR_POS
        
        for i in range(0,num):
            self.checkResize(self.cursorY + self.allElements[i].get_height())
            self.image.blit(self.allElements[i].getImage(), self.allElements[i].getBlitPos())
            self.cursorY += self.allElements[i].get_height() + self.CURSOR_BORDER_INCREMENT        

    def checkResize(self, potentialCursorY = None):
        if potentialCursorY == None:
            potentialCursorY = self.cursorY
            
        if potentialCursorY > (self.imageMaxY - 150):
            # need to resize window
            self.imageMaxY *= 2                    
            newImage = pygame.Surface((self.imageMaxX, self.imageMaxY))
            # put the old image onto the new image at top left
            newImage.blit(self.image, (0,0))
            self.image = newImage

    #def isClicked(self, command, recipeID, recipeData = None):
    def isClicked(self, xy):        
        ## first things first, we need to change the xy point from a coordinate on the entire screen
        # to a coordinate relative to the top left of the scrollable window box

        x,y = xy
        y -= self.rect.top
        xy = x,y
        
        for sprite in self.allElements:
            if sprite.getRect().collidepoint(xy):
                # each "element" will be equipped with collidePoint
                buttonClicked = sprite.collideButtons(xy)
                #print "Relative Position is: ", xy                
                
                if buttonClicked == None:
                    return
                else:
                    # a list of the ID values in sprite
                    # if identity is delete it will also have a number
                    # seperated by a space, of the reference to be deleted
                    parseID = buttonClicked.getIdentity().split()
            
                    # if the parseID is just 1, then the button is for a change
                    # in state, and we need to return immediately and tell the main program
                    # this information
                    if len(parseID) == 1:
                        return parseID
                    
                    else:
                        # state contains a reference number , meaning we have
                        # to do something within this state
    
                        ### need to enforce strict discipline on names                        
                        command = parseID[0].split("@")
                            
                        recipeID = command[1]
                        for i in range(1,len(parseID)):
                            recipeID += " " + parseID[i]

                        ## if we are expanding the button, we need to also send
                        # the recipe information so it can be put on the screen
                        recipeInfo = None
                        if command[0] == "expand":
                            command[1] = recipeID
                            return command
                        elif command[0] == "unExpand":
                            self.removeElement(recipeID, "textBlock")
                            return None
                        elif command[0] == "addToGroceryList" or command[0] == "removeFromGroceryList":
                            command[1] = recipeID
                            sprite.toggleButton("groceryButton")
                            self.redrawAll()
                            return command

        # default behavior for this, returns None if no buttons were hit or w.e
        return None        

    def removeElement(self, nameToRemove, t):
        if t == "textBlock":
            for i,sprite in enumerate(self.allElements):
                if sprite.getName() == nameToRemove and isinstance(sprite, Row):
                    sprite.toggleButton("unExpand")
                    break

            i += 1
            sprite = self.allElements.pop(i)
            #print "THE SPRITE IN QUESTION IS: ", sprite

            for counter in range(i, len(self.allElements)):                
                self.allElements[counter].updateY(-(sprite.get_height() + self.CURSOR_BORDER_INCREMENT))

        self.redrawAll()

    def addTextBlock(self, name, data):
        ## name is the name of recipe this textBlock refers to
        # should be able to find that name within the list of allElements

        # first we find the row that has the name of the recipe data we are adding
        for i,sprite in enumerate(self.allElements):
            if sprite.getName() == name:
                sprite.toggleButton( "expand")
                i += 1
                break

        # add the recipe data textBlock right after that row,@ sprite.rect. bottom
        newTextBlock = TextBlock(name, data, self.theFont,
                                 sprite.getRect().bottom + self.CURSOR_BORDER_INCREMENT)

        for counter in range(i,len(self.allElements)):
            #print self.allElements[counter], " @ ", self.allElements[counter].getRect().top,
            self.allElements[counter].updateY(newTextBlock.get_height() + self.CURSOR_BORDER_INCREMENT)

        self.allElements.insert(i, newTextBlock)
        self.redrawAll()

    def getRect(self):
        return self.rect

    def scroll(self, dy):
        self.rect.top += dy
        
        #for element in self.allElements:
        #    element.updateY(dy)
            
        self.redrawAll()

    def updateState(self, toggledRecipeNames):
        print "pre-toggled recipes are: ", toggledRecipeNames
        if isinstance(toggledRecipeNames, str):
            temp = toggledRecipeNames
            toggledRecipeNames = []
            toggledRecipeNames.append(temp)

        for recipe in toggledRecipeNames:
            print
            print
            print "checking recipe: ", recipe
            for element in self.allElements:
                if isinstance(element, Row):
                    print "     comparing to: ", element.getName()
                    if element.getName() == recipe:
                        print "     match!!"
                        element.toggleButton("groceryButton")

            self.redrawAll()

    def grabState(self):
        ## see main.py for comments
        if self.mode == "recipeViewer":
            toggledRows = []
            for element in self.allElements:
                if isinstance(element, Row):
                    #print "     looking @ ", element.getName(), "   is it toggled? ", element.isAddedToGroceryList()
                    if element.isAddedToGroceryList():
                        toggledRows.append(element.getName())
                        #print "     storing ", element.getName()
            return toggledRows
            

        elif self.mode == "groceryListViewer":
            ingredientList = []
            for element in self.allElements:
                print "checking this now: ", element.getName()
                if isinstance(element, Row):
                    ingredientList.append(element.getModifiedIngredient())
            return ingredientList
                    
        
