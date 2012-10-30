#! /usr/bin/env/ python

import pygame
from pygame.locals import *
from pygame import sprite

from utils import loadImage
from pygame.sprite import Sprite
from pygame.sprite import Group

from ingredient import Ingredient

class RecipeReciever(Sprite):
    def __init__(self, mode, imgdir, ingParser):
        Sprite.__init__(self)

        self.fields = [["Title","Instructions","IngredientList","Description","Rating"],
                  [True,True,True,True,True]]

        self.focus = None
        self.allTextBoxes = []
        self.allButtons = []
        self.recipeDict = {}
        self.belowTextBorder = 50
        self.imgFolder = imgdir

        ## we might need to create this in the main program
        # when we implement the database of keywords
        # so we can pass them to the parser withotu passing them here first
        # but for now this is ok
        self.ingredientParser = ingParser

        # store None so we can know wether to erase it or not
        self.imageCreated = False

        self.state = "awaitingInput"

        if not pygame.font.get_init():
            pygame.font.init()
        self.theFont = pygame.font.Font(None, 30)
        
        if mode == "addRecipePage":
            self.createImage()

            self.rect = self.image.get_rect()

    def createImage(self):
        if self.imageCreated:
            self.image.fill((0,0,0))

        self.allTextBoxes = []
        self.allButtons = []
            
        totalHeight = 10
        i = 0
        doneCount = 0
        print "FIELDS:", self.fields[0]
        print "       ", self.fields[1]
        #tally the height
        for f in self.fields[0]:
            self.allTextBoxes.append(TextBlock(f + ":", f + ":", self.theFont, totalHeight))

            if self.fields[1][i]:
                self.allButtons.append(Button(self.imgFolder, "textButton",
                                (self.allTextBoxes[i].getImage().get_width() + 15, totalHeight),
                                            f, -1))
                self.allButtons[i].addText("Add Data")
            else:
                self.allButtons.append(Button(self.imgFolder, "checkBox",
                                (self.allTextBoxes[i].getImage().get_width() + 15, totalHeight),
                                            "nothing", -1))
                doneCount += 1
            
            totalHeight += self.allTextBoxes[i].getImage().get_height() + self.belowTextBorder
            i+=1

        totalHeight += 120
        self.image = pygame.Surface((400, totalHeight))
                
        for button in self.allButtons:
            self.image.blit(button.getImage(), button.getRect())
        for text in self.allTextBoxes:
            self.image.blit(text.getImage(), text.getRect())

        if doneCount >= 5:
            doneButton = Button(self.imgFolder, "textButton", (150, totalHeight - 100),
                                       "submitRecipe", -1)
            doneButton.addText("Submit Recipe")
            self.allButtons.append(doneButton)
            self.image.blit(doneButton.getImage(), doneButton.getRect())
            
        self.imageCreated = True
            
    def isClicked(self, xy):
        # need to scale the xy value to be relative to the recipeReciever window
        x,y = xy
        x -= self.rect.left
        y -= self.rect.top
        xy = x,y
        
        ## awaitingInput is the main screen with all the various buttons
        if self.state == "awaitingInput":    
            found = False
            for button in self.allButtons:
                if not button.getIdentity() == "nothing":
                    if button.getRect().collidepoint(xy):
                        if not button.getIdentity() == "submitRecipe":
                            self.openTextBox(button.getIdentity())
                        else: ## send the recipe back to the main program
                            return self.recipeDict
                    
        elif self.state == "inTextBox":
            infoReturned = self.textBox.isClicked(xy)
            if not (infoReturned == None):
                if self.textBox.getIdentity() == "IngredientList":
                    ## in case s is one giant string, as it probably will be
                    # we need to break it up into individual lines,
                    # based on the split characters, which seem to be
                    # /n for python but /r for everything else

                    ## need to create some kind of error catching here as well
                    # and everywhere just in case there is illegal input
                    # but we will do that later
                    print "info Returned: "
                    print infoReturned                    

                    ## the general format is this:
                    # ingredientParser.passString(infoReturned)
                    #       info returned is a giant block of text
                    #       subdivided by /r/n or /n, into individual lines
                    #       each containing an ingredient

                    ## result = ingredientParser.parse()
                    #       this returns the progress of the ingredientParser
                    #       for example, if the parser is stuck on something
                    #       it will put in its "message" field info regarding
                    #       asking clarification of the user, which can then
                    #       be handled by the GUI
                    #       -- otherwise this will return an "done" which is
                    #       then tells the GUI to get the finishedMessage

                    self.ingredientParser.passString(infoReturned)
                    result = self.ingredientParser.parse()
                    while (not (result == "done")):
                        result = self.ingredientParser.parse()

                    # this data needs to be in the form
                    # name?(, modifiers) amount unitString
                    ## NOT IN INGREDIENT OBJECT FORM!
                    infoReturned = self.ingredientParser.getFinishedIngredientList()
                        
                    print
                    print
                    print "the new info returned:"
                    print infoReturned

                    fieldName = "IngredientList"
                

                    #ping!!!

                    ## make a GUI Error here (bad InputError) or something
                    # that when they enter ingredients it checks they
                    # are of the right format... or throws an error
                    # and pulls up the AlertBox (which we have yet to make)
                    # that tells the user of their mistake.

                    # this alert box also should be the same class that confirms
                    # deleting recipes and such...


                ##  from now on, we should always clarify in comments what is being
                # returned in complex situations like this
                # recipeDict goes back to the main program, whereupon
                # Main send the dictionary to Recipe.fromDictionary(recipeDict)
                # which then goes to Ingredient.fromString()                
                self.recipeDict[self.textBox.getIdentity()] = infoReturned
                i = self.fields[0].index(self.textBox.getIdentity())
                self.fields[1][i] = False
                self.createImage()
                self.state = "awaitingInput"
                                        

    def recieveClipboardPaste(self, string):
        if self.state == "inTextBox":
            self.textBox.addText(string)
            self.image.blit(self.textBox.getImage(), self.textBox.getRect())

    def openTextBox(self, label):
        self.state = "inTextBox"
        self.imageStorage = self.image
        self.textBox = TextBox(label,(600,600), (15,15), self.theFont, self.imgFolder)
        self.image.fill((0,0,0))
        self.image.blit(self.textBox.getImage(), self.textBox.getRect())
