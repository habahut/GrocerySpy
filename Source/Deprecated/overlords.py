#! usr/bin/env/ python

import json, os, sys
from os.path import abspath, dirname

from groceryList import GroceryList
import pygame
from pygame.locals import *

from recipe import Recipe

import winshell

class DataBaseManager(object):
    """
    all the database will live within this class,
    so when the program starts this class will read the necessary data from
    the file and store it in memory
    """

    def __init__(self, directory):
        self.DIRECTORY = directory
        self.ROOT_DIR = os.path.dirname(sys.argv[0])
        print "root", self.ROOT_DIR
        self.dataBasePath = os.path.join(self.ROOT_DIR,  directory)
        print
        print "path", self.dataBasePath

        """
        each recipe is in its own file. Within each file is a dictionary
        self.allRecipes is a dictionary where the keys are the recipe title
        and the values are dictionaries that contain all the information about
        each recipe
        """
        # this contains only the recipes that have so far been loaded
        # from memory

        ## this is of the form "RecipeName" : "Recipe Object"
        self.loadedRecipes = {}

    def loadRecipe(self, recipeTitle):
        recipePath = os.path.join(self.dataBasePath, recipeTitle + ".json")
        print "recipe path==--=", recipePath

        try:
            f = open(recipePath, "r")
            data = json.load(f)
            f.close()

            print
            print
            print data
            print
            print


            r = Recipe.fromDictionary(data)
            print "HERE IS THE RECIPE"
            theRecipeString = r.writeToReadableString()
            print theRecipeString
            return theRecipeString
            
        except IOError:
            print "no such file"

    def addRecipeDictionaryToLoadedRecipes(self, recipeDict):
        self.loadedRecipes[recipeDict['Title']] = recipeDict

    def writeRecipesToFile(self, recipeList):
        self.addRecipesToDict(recipeList)

        for recipeName, recipeDictionary in self.loadedRecipes.iteritems():
            print recipeName
            for k in recipeDictionary.keys():
                print k,":",recipeDictionary[k]

        # all the recipes to be added have been combined into one dictionary
        # now we need to go through that dictionary and put each recipe into its own
        # file
        for recipe,recipeDictionary in self.loadedRecipes.iteritems():
            print
            print recipe
            thisRecipePath = os.path.join(self.dataBasePath, recipeDictionary['Title']+ ".json")
            f = open(thisRecipePath,"w")
            data = json.dumps(recipeDictionary)
            f.write(data)
            f.close()


    def addRecipesToDict(self, recipeList):
        currentRecipes = self.loadedRecipes.keys()
        
        for recipe in recipeList:
            recipeName = recipe.getName()
            alreadyInDict = False

            for name in currentRecipes:
                if name == recipeName:
                    alreadyInDict = True
                    break

            if not alreadyInDict:
                self.loadedRecipes[recipeName] = recipe.writeToDictionary()

    ## this is where we call recipeToReadableString!!
    # the dictionary stored in this class holds no recipe objects
    # this class actually holds on references to the recipe objects themselves
    # recipeList will need to be passed in by the GUI Overlord
    def writeRecipesToDesktop(self, recipeList):
        desktopPath = winshell.desktop()
        desktopPath = os.path.join(desktopPath, 'test.txt')
        target= open(desktopPath, 'a')

        readableRecipeString = ""
        for recipe in recipeList:
            readableRecipeString += recipe.writeToReadableString()

        # note, every time this runs it appends to the text file,
        # does not erase what is already there!
        target.write(readableRecipeString)

    def displayAllRecipes(self):
        allRecipeNames = ""

        for filename in os.listdir(self.dataBasePath):
            recipe_Name, extension = filename.split('.')

            ### apparently can just include spaces, no need to transform them
            ### to underscores
            #recipeWords = recipe_Name.split("_")
            #recipeName = ""
            #for word in recipeWords:
            #    recipeName += word

            allRecipeNames += recipeName + "\n"

        return allRecipeNames

    def displayAllLoadedRecipes(self):
        print "GOT HERE"
        for recipeName, recipeDictionary in self.loadedRecipes.iteritems():
            print recipeName
            for k in recipeDictionary.keys():
                print k,":",recipeDictionary[k]
    


####
#
#  need some interaction between choosing what recipes are printed
#  and just printing recipes
#  also printing grocery lists...
#  maybe have some function to store popular grocery lists?
####



## need to start developing the GUI Master
# making the DBM and GUI communicate is going to be difficult probably...

# maybe the GUI master will instantiate its own dataBaseManager,
# that way the GUI can control the DBM and do all the
# information passing internally...
# probably will be the easiest way

# GUIOverlord should be a singleton ideally, should not be able to run more than
# one of this program at a time....

class GUIOverlord(object):
    """
    creates and recieves input from the GUI
    """

    def __init__(self):
        """
        no gui stuff yet, finishing the core components
        """

        pass

    def printGroceryList(self, recipeList):
        groceryList = GroceryList(recipeList)

        for item in groceryList.getList():
            print item.toString()

    
                
            



            
