#! usr/bin/env/ python


import json, os, sys
from os.path import abspath, dirname

from recipe import Recipe

class DataBaseManager(object):
    """
    all the database will live within this class,
    so when the program starts this class will read the necessary data from
    the file and store it in memory
    """

    def __init__(self, dbPath):
        #self.DIRECTORY = directory
        #self.ROOT_DIR = os.path.dirname(sys.argv[0])
        #print "root", self.ROOT_DIR
        #self.dataBasePath = os.path.join(self.ROOT_DIR,  directory)
        #print
        #print "path", self.dataBasePath

        self.dataBasePath = dbPath
        self.recipeDataBasePath = os.path.join(dbPath, "Recipes")
        self.recipeParserPath = os.path.join(dbPath, "RecipeParsingInfo")

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
        recipePath = os.path.join(self.recipeDataBasePath, recipeTitle + ".json")

        try:
            f = open(recipePath, "r")
            data = json.load(f)
            f.close()
            r = Recipe.fromDictionary(data)
            return r
        except IOError:
            print "no such file"

    def addRecipeToDataBase(self, recipe):        
        # all the recipes to be added have been combined into one dictionary
        # now we need to go through that dictionary and put each recipe into its own
        # file
        fileName = recipe.getName()
        fileName = fileName.replace("\n","")
        fileName = fileName.replace("\r","")
        
        thisRecipePath = os.path.join(self.recipeDataBasePath, fileName+ ".json")
        f = open(thisRecipePath,"w")
        data = json.dumps(recipe.writeToDictionary())
        f.write(data)
        f.close()

    ## this string should see if the file exists already
    # and then delete it if it does, so it doesn't append
    def writeStringToDesktop(self, String, name):
        desktopPath = os.path.join("~", "Desktop", name +".txt")
        desktopPath = os.path.expanduser(desktopPath)

        try:
            os.remove(desktopPath)
        except WindowsError:
            pass
        
        target = open(desktopPath, 'a')

        target.write(String)
        target.close()
        
    def writeRecipeToDesktop(self, recipeName):        
        recipe = self.loadRecipe(recipeName)
        self.writeStringToDesktop(recipe.toReadableString(), recipeName)        

    def deleteRecipe(self, recipeName):
        thisRecipePath = os.path.join(self.recipeDataBasePath, recipeName+ ".json")
        os.remove(thisRecipePath)

    ## returns the names of all the recipes in the database
    def getAllRecipes(self):
        allRecipeNames = []

        for filename in os.listdir(self.recipeDataBasePath):
            recipeName, extension = filename.split('.')

            ### apparently can just include spaces, no need to transform them
            ### to underscores
            allRecipeNames.append(recipeName)

        return allRecipeNames

    def getRandomRecipe(self):
        allRecipeNames = self.getAllRecipes()

        return allRecipeNames[0]

    def loadParserDataFields(self):
        allFields = {}
        for filename in os.listdir(self.recipeParserPath):
            try:
                f = open(os.path.join(self.recipeParserPath, filename), "r")
                data = json.load(f)
                f.close()

                fieldName,extension = filename.split('.')
                allFields[fieldName] = data[fieldName]
            except IOError:
                print "file read error, ", filename," skipped."

        return allFields

    def writeNewParserDataField(self, fieldName, fieldData):
        try:
            dictWrapper = {}
            dictWrapper[fieldName] = fieldData
    
            f = open(os.path.join(self.recipeParserPath, fieldName +".json"), "w")
            data = json.dumps(dictWrapper)
            f.write(data)
            f.close()
        except IOError:
            print "ERROR writing ParserData to", filename

    def addDataToParserField(self, fieldName, stringList):
        try:
            f = open(os.path.join(self.recipeParserPath, fieldName +".json"), "r")
            data = json.load(f)
            if fieldName in data.keys():
                if isinstance(stringList,str):
                    data[fieldName].append(stringList)
                else:
                    for s in stringList:
                        data[fieldName].append(s)
            else:
                raise InputException("fieldName does not match File")

            self.writeNewParserDataField(fieldName, data[fieldName])
            f.close()
        except IOError:
            pass

class InputException(Exception):
    def __init__(self, value):
        self.v = value
    def __str__(self):
        return repr(self.value)
    

if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(sys.argv[0])
    DATA_DIR = os.path.join(ROOT_DIR, "database")
    p = DataBaseManager(DATA_DIR)

    p.writeRecipesToDesktop(p.loadRecipe("Crock Pot Chili"))

    """d = ["green", "red", "orange", "blue", "spicy", "large", "chopped", "big"]
    p.writeNewParserDataField("PreModifiers", d)

    p.addDataToParserField("PreModifiers", "huge")
    print "==================================="
    print
    print p.loadParserDataFields()"""

    




    



