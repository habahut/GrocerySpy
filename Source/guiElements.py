#! /usr/bin/env/ python

import pygame
from pygame.locals import *
from pygame import sprite

from utils import loadImage
from pygame.sprite import Sprite
from pygame.sprite import Group

from ingredient import Ingredient

import os


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
        self.theFont = pygame.font.Font("freesansbold.ttf", 15)
        #self.theFont = pygame.font.SysFont(None, 30)

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

    



#### make a settigns file that all static data goes in,
# i.e. screen size, folder information etc....    

 
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
        self.theFont = pygame.font.Font("freesansbold.ttf", 30)
        #self.theFont = pygame.font.SysFont(None, 30)
        
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
        textBox = TextBlock("doesntMatter", string, self.theFont, 15, self.height - 70)
        self.image.blit(textBox.getImage(), textBox.getRect())

    def getRect(self):
        return self.rect

    def getImage(self):
        return self.image




    
            
