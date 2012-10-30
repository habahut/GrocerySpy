#! usr/bin/env/ python

import pygame
from pygame.locals import *

import os, sys

from groceryList import GroceryList
from dataBaseManager import DataBaseManager
from recipe import Recipe
from ingredient import Ingredient
from ingredientParser import IngredientParser

from pygame import sprite
from pygame.sprite import Group

import pygame
from pygame.locals import *

from utils import loadImage

import pyperclip

from button import Button
from scrollableWindow import ScrollableWindow
from recipeReciever import RecipeReciever
from textBox import TextBox
####
#
#  need some interaction between choosing what recipes are printed
#  and just printing recipes
#  also printing grocery lists...
#  maybe have some function to store popular grocery lists?
####


"""
might be useful later
sys.path[0] alone will give you the directory without the scriptname.
"""

     


class Main(object):
    """
    creates and recieves input from the GUI
    """

    SCREEN_SIZE = 800,600
    FPS = 30

    def __init__(self):
        """
        no gui stuff yet, finishing the core components
        """

        self.ROOT_DIR = os.path.dirname(sys.argv[0])
        self.IMG_DIR = os.path.join(self.ROOT_DIR, "images")
        self.DATA_DIR = os.path.join(self.ROOT_DIR, "database")
        self.dbm = DataBaseManager(self.DATA_DIR)        
        
        pygame.init()
        pygame.font.init()
        
        self.MAIN_SCREEN = pygame.display.set_mode(self.SCREEN_SIZE)
        self.MAIN_SCREEN_RECT = self.MAIN_SCREEN.get_rect()

        self.openingImage,self.openingImageRect = loadImage(self.IMG_DIR, "GrocerySpy.jpg")

        self.MAIN_SCREEN.blit(self.openingImage,
                         (self.MAIN_SCREEN_RECT.centerx - self.openingImageRect.width /2,
                          self.MAIN_SCREEN_RECT.centery - self.openingImageRect.height /2))

        ## make button here
        startButton = Button(self.IMG_DIR, "textButton", (300,475), "menu", -1)
        startButton.addText("Start Here")

        # add that button to the list
        self.buttonGroup = Group(startButton)
        self.windowGroup = Group()

        self.state = "prestart"
        self.stateChanged = False

        # set key repeats for scrolling windows
        pygame.key.set_repeat(20, 20)

        self.groceryList = GroceryList()

        # variable for storing the state of the browseAll window if it is left
        self.toggledRecipeNames = []

        self.controlHeld = False
        self.pasteDelayReset = 1000
        self.pasteDelay = self.pasteDelayReset

    def run(self):
        done = False
        while not done:
            ## input loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    done = True

                ## right click anything to have a pop up window
                # appear at the cursor with more information about the thing                    
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.handleLeftMouseClick(pygame.mouse.get_pos())

                ## arrow keys
                elif event.type == KEYDOWN and event.key == K_DOWN:
                    self.attemptScroll(-3)
                elif event.type == KEYDOWN and event.key == K_UP:
                    self.attemptScroll(3)

                elif event.type == KEYDOWN and (event.key == K_RCTRL or event.key == K_LCTRL):
                    self.controlHeld = True
                elif event.type == KEYUP and (event.key == K_RCTRL or event.key == K_LCTRL):
                    self.controlHeld = False
                elif event.type == KEYDOWN and event.key == K_v:
                    if self.controlHeld:
                        if self.pasteDelay < 10:
                            self.doPaste()
                            self.pasteDelay = self.pasteDelayReset
            ## end input

            if self.pasteDelay > 0:
                self.pasteDelay -= 1

            ## change screen
            if self.stateChanged:
                ## clear everything on the screen first
                self.buttonGroup.empty()
                self.windowGroup.empty()
                self.MAIN_SCREEN.fill((0,0,0))
                
                self.stateChanged = False
                if self.state == "menu":
                    self.createMenu()
                elif self.state == "browseAll":
                    self.setUpViewAll()
                elif self.state == "viewGroceryList":
                    self.setUpViewGroceryList()
                elif self.state == "addRecipe":
                    #print "here"
                    self.setUpRecipeAdder()
                elif self.state == "search":
                    self.setUpSearchTextBox()
                elif self.state == "deleteRecipe":
                    self.setUpDelete()
                elif self.state == "exit":
                    done = True
                    
                    
                    
                ## do stuff to update the new state

            # after updates, draw
            self.buttonGroup.draw(self.MAIN_SCREEN)
            self.windowGroup.draw(self.MAIN_SCREEN)

            pygame.display.flip()

        pygame.quit()

    def setUpViewAll(self):
        x,y = self.SCREEN_SIZE
        x-=100
        viewAllWindow = ScrollableWindow(self.IMG_DIR, (x,y),self.SCREEN_SIZE, "recipeViewer")

        viewAllWindow.addText(self.dbm.getAllRecipes())
        #viewAllWindow.addText(self.dbm.getRandomRecipe())

        viewAllWindow.updateState(self.toggledRecipeNames)
        self.windowGroup.add(viewAllWindow)

        backButton = Button(self.IMG_DIR, "backButton", (705,30), "menu", -1)
        self.buttonGroup.add(backButton)

        ## in one command, we call getAllRecipes() on the DBM, returning
        # a string list of all the names, and pass that to the
        # scrollable window to add that text to the thing
        # this returns the expandButtons for each row, which we add
        # to the buttonGroup

    def setUpDelete(self):
        x,y = self.SCREEN_SIZE
        x-=100
        viewAllWindow = ScrollableWindow(self.IMG_DIR, (x,y),self.SCREEN_SIZE, "recipeDeleter")
        viewAllWindow.addText(self.dbm.getAllRecipes())
        self.windowGroup.add(viewAllWindow)

        backButton = Button(self.IMG_DIR, "backButton", (705,30), "menu", -1)
        self.buttonGroup.add(backButton)
                            

    def setUpViewGroceryList(self):
        x,y = self.SCREEN_SIZE
        x-=100
        viewAllWindow = ScrollableWindow(self.IMG_DIR, (x,y),self.SCREEN_SIZE, "groceryListViewer")
        self.windowGroup.add(viewAllWindow)

        backButton = Button(self.IMG_DIR, "backButton", (705,30), "menu", -1)
        self.buttonGroup.add(backButton)

        viewAllWindow.addGroceryList(self.groceryList.getAllIngredients())

        writeDesktopButton = Button(self.IMG_DIR, "writeToDesktop", (705,80), "writeToDesktop", -1)
        self.buttonGroup.add(writeDesktopButton)
        
    def setUpRecipeAdder(self):
        ingParser = IngredientParser()#self.dbm.loadParserDataFields())
        recipeAdderWindow = RecipeReciever("addRecipePage",self.IMG_DIR, ingParser)
        self.windowGroup.add(recipeAdderWindow)

        backButton = Button(self.IMG_DIR, "backButton", (705,30), "menu", -1)
        self.buttonGroup.add(backButton)
        

    """def setUpSearch(self):
        self.windowGroup.add(TextBox(

    #def setUpSearchTextBox(self):"""
        
        

    def doPaste(self):
        if self.state == "addRecipe":
            (self.windowGroup.sprites())[0].recieveClipboardPaste(pyperclip.paste())

    def attemptScroll(self, dy):
        for sprite in self.windowGroup.sprites():
            sprite.scroll(dy)                

    def handleLeftMouseClick(self, xy):        
        for button in self.buttonGroup.sprites():
            if button.getRect().collidepoint(xy):
                ## stupid organization leads to hacky solutions...
                # in groceryList viewer, the writeToDesktop button must be stored in the main
                # class. So thats whats going on here, we call writeToDesktop
                # in the scrollable window and grab the grocery list there and send that to
                # dbm to write it to desktop
                if button.getIdentity() == "writeToDesktop":
                    theString = self.windowGroup.sprites()[0].writeToDesktop()
                    #print
                    #print
                    #print theString
                    self.dbm.writeStringToDesktop(self.windowGroup.sprites()[0].writeToDesktop(), "Grocery List")
                    self.state = "menu"
                    self.stateChanged = True
                    #print "got here!"
                    return                

                
                ## we want to store the state of the stuff people are looking at
                # whether that is a grocery list they have increased or recipes they have added to cart
                # we call the "grabState()" method of the scrollableWindow to get the information

                #### keep in mind, this is the previous state
                # so if self.state == "browseAll" it means we are coming from browseAll state
                # to the menu          
                if self.state == "browseAll":
                    ## this one is tricky. We need to store a list of toggled rows, and then
                    # if the user goes back to the viewAllBrowser we need to call "updateState()"
                    # with this list, to ensure those buttons are toggled to reflect that they are
                    # still in the groceryList

                    # keep in mind this is a list of the names of the recipes that are already added
                    # so we will need to search for them in "updateState()"
                    allWindows = self.windowGroup.sprites()
                    if allWindows:
                        self.toggledRecipeNames = allWindows[0].grabState()

                elif self.state == "viewGroceryList":
                    ## this one is simple, we just grabState() and store the returns in self.groceryList
                    # all the changes the user has made will be in the new list
                    # and new changes will happen to that list
                    allWindows = self.windowGroup.sprites()
                    if allWindows:
                        self.groceryList.empty()
                        self.groceryList.addIngredientList(allWindows[0].grabState())
                        
                self.state = button.getIdentity()
                self.stateChanged = True

        command = None
        if self.state == "browseAll" or self.state == "deleteRecipe":
            for scrollableWindow in self.windowGroup.sprites():
                if scrollableWindow.getRect().collidepoint(xy):
                    command = scrollableWindow.isClicked(xy)
                    break

            if not command == None:
                ## command is a string, meaning there is a change of state
                # from the button press
                #print "command recieved!"
                #print "     ", command
                if isinstance(command, str):
                    self.state = command
                    self.stateChanged = True
                    #print "this thing"
                else:
                    if len(command) == 2:
                        #print "entered here"
                        #print "command[0]:", command[0]
                        if command[0] == "expand":
                            recipeInfo = self.dbm.loadRecipe(command[1]).toReadableString()
                            scrollableWindow.addTextBlock(command[1], recipeInfo)
                        elif command[0] == "addToGroceryList":                            
                            self.groceryList.addRecipe(self.dbm.loadRecipe(command[1]))
                        elif command[0] == "removeFromGroceryList":
                            self.groceryList.removeRecipe(self.dbm.loadRecipe(command[1]))
                        elif command[0] == "writeToDesktop":
                            #print "got into this"
                            self.dbm.writeRecipeToDesktop(command[1])
                        if command[0] == "delete":
                            #print "got here"
                            self.dbm.deleteRecipe(command[1])

        elif self.state == "menu" or self.state=="prestart":
            for sprite in self.buttonGroup.sprites():
                if sprite.rect.collidepoint(xy):
                    
                    parseID = sprite.getIdentity().split()
            
                    # no extra info, just an ID for the new state
                    # if this is not true there is something wrong
                    if len(parseID) == 1:
                        spriteID = parseID[0]
                        if not spriteID == self.state:
                            self.state = spriteID
                            self.stateChanged = True
                    else:
                        raise GUIError("button gives too much data")        

        elif self.state == "addRecipe":
            for recipeReciever in self.windowGroup.sprites():
                recipeData = recipeReciever.isClicked(xy)
                if not recipeData == None:
                    #for k in recipeData.keys():
                        #print k, recipeData[k]
                    self.dbm.addRecipeToDataBase(Recipe.fromDictionary(recipeData))
                    self.state = "menu"
                    self.stateChanged = True

        elif self.state == "viewGroceryList":
            for scrollableWindow in self.windowGroup.sprites():
                command = scrollableWindow.isClicked(xy)


        elif self.state == "search":
            ## search has 2 states, the first is a text box where the user
            # enters what the search ingredient is
            # the second the window where the results are displayed
            # we determine which state by what is in self.windowGroup.sprites()
            # a TextBox is the first state, a ScrollableWindow is the second
            for sprite in self.windowGroup.sprites():
                pass#command = sprite.isClicked
                
    def createMenu(self):
        browseButton = Button(self.IMG_DIR, "textButton", (10,75), "browseAll", -1)
        browseButton.addText("Browse All")
        self.buttonGroup.add(browseButton)

        #searchButton = Button(self.IMG_DIR, "textButton", (210,75), "search", -1)
        #searchButton.addText("Search")
        #self.buttonGroup.add(searchButton)

        addRecipeButton = Button(self.IMG_DIR, "textButton", (410,75), "addRecipe", -1)
        addRecipeButton.addText("Add Recipe")
        self.buttonGroup.add(addRecipeButton)

        deleteRecipeButton = Button(self.IMG_DIR, "textButton", (10,275), "deleteRecipe", -1)
        deleteRecipeButton.addText("Delete Recipe")
        self.buttonGroup.add(deleteRecipeButton)

        groceryListButton = Button(self.IMG_DIR, "textButton", (210,275), "viewGroceryList", -1)
        groceryListButton.addText("View Cart")
        self.buttonGroup.add(groceryListButton)

        exitButton = Button(self.IMG_DIR, "textButton", (410, 275), "exit", -1)
        exitButton.addText("Exit")
        self.buttonGroup.add(exitButton)



class GUIError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
            
