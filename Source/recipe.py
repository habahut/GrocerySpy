#! /usr/bin/env python

from ingredient import Ingredient


class Recipe(object):

    def __init__(self, ril, t, dL, iL, r = "unknown"):
        self.ingredientList = ril
        self.description = dL
        self.rating = r
        self.title = t
        self.instructions = iL

    @classmethod
    def fromDictionary(cls, dictionary):
        title = dictionary["Title"].replace("\r","")
        title = title.replace("\n","")
        rating = dictionary["Rating"]
        instructions = dictionary["Instructions"]
        ingredientStrings = dictionary["IngredientList"]
        description = dictionary["Description"]
        
        ingredientList = []
        for s in ingredientStrings:
            newIngredient = Ingredient.fromString(s)
            if not newIngredient == None:
                ingredientList.append(newIngredient)

        return cls(ingredientList, title, description, instructions, rating)

    def getName(self):
        return self.title

    def getIngredientList(self):
        return self.ingredientList        
    
    def getRating(self):
        return self.r

    def setRating(self, r):
        self.rating = r

    def getItemList(self):
        return self.ril

    def getDescription(self):
        return self.description
    
    def scale(self,d):
        self.quantity /= d
        ## need to go through all quantities and set them to the new value


    """
    two different methods here
    one writes this recipe to a dictionary for storage
    the other writes it in a readable form for a human recipient
    """
    # this writes to the dictionary for storage
    def writeToDictionary(self):
        theDictionary = {}

        ## need to figure out a way to go from ingredient objects to
        # strings for each ingredient, and also back again
        allIngredientList = []
        for ingredient in self.ingredientList:
            allIngredientList.append(ingredient.toString())
            
        theDictionary['IngredientList'] = allIngredientList
        theDictionary['Description'] = self.description
        theDictionary['Rating'] = self.rating
        theDictionary['Title'] = self.title
        theDictionary['Instructions'] = self.instructions

        return theDictionary

    def addLineBreaksToParagraph(self, paragraph):
        eachWord = paragraph.split(" ")
        characterCount = 0

        bigString = ""
        
        for s in eachWord:
            characterCount += s.__len__() + 1
            if characterCount >= 45:
                characterCount = 0
                bigString += "\n"
            bigString += s + " "

        return bigString + "\n"
                


    ## this writes to a readable string
    def toReadableString(self):        
        borderRow = ""
        for i in range(len(self.title) + 4):
            borderRow += "-"
            
        theBigString = borderRow + "\n"
        theBigString += "- " + self.title + " - \n"
        theBigString += borderRow + "\n \n"
   

        theBigString += "description: \n"
        if (isinstance(self.description, str) or isinstance(self.description, unicode)):
            theBigString += self.addLineBreaksToParagraph(str(self.description))
        else:
            for i in range(len(self.description)):
                theBigString += self.description[i] + "\n"

        theBigString += "\n"
        theBigString += "ingredients: \n"
        for ingredient in self.ingredientList:
            theBigString += ingredient.getReadableName() + "\n"
            
        theBigString += "\n"
        theBigString += "instructions:  \n"
      
        if (isinstance(self.instructions, str) or isinstance(self.instructions, unicode)):
            theBigString += self.addLineBreaksToParagraph(str(self.instructions))
        else:
            for i in range(len(self.instructions)):
                theBigString += self.instructions[i] + "\n"

        theBigString += "\n"
        
        theBigString += "rated: " + str(self.rating) + "/5  \n\n"

        return theBigString

    ## prints the entire recipe
    def toString(self):
        toPrint = " "
        print
        for i in range(len(self.title) + 4):
            toPrint += "-"
        print toPrint
        print "- ", self.title, " -"
        print toPrint
   

        print
        print
        print "description:"
        for i in range(len(self.description)):
            print self.description[i]
        print
        print "ingredients:"
        for ingredient in self.ingredientList:
            print ingredient.toString()
            
        print
        print "instructions:"
        for i in range(len(self.instructions)):
            print self.instructions[i]

        print
        
        print "rated: ",self.rating, "/5"
        print


    """
-=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=-
-=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=-
-=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=-
-=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=-
-=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=-
-=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=--=-==--=-=-=-
    """ 

    ##old code, prices and stuff

    """ should include some kind of price guessing algorith
        so maybe guess what the price may be if it is missing from one store,
        by averaging the other prices?
    """
    """
        things left to do for this:
        fix the price print out: it prints out the price per unit but doesn't actually calculate the right price
        i.e.: need 5 x chicken(lbs) but only adds 1x chicken
        also formatting.....
    """
    ## prints the price list, calculating and displaying the price at all stores
    def printPriceList(self):
        storeNames = self.allPossibleStores()
        
        #prepare the tallies
        pricePerStore = []
        storePriceAsterisks = []
        for store in storeNames:
            pricePerStore.append(0)
            storePriceAsterisks.append(" ")

        # print each store
        print " "*15,
        for i in range(len(storeNames)):
            toPrint = "|" + storeNames[i].center(15)
            print toPrint,

        # border row
        print ""
        print "="*16,
        for i in range(len(storeNames)):
            print "="*16, 
        print ""

        # print each ingredient and the price at each store
        for ingredient in self.ingredientList:
            toPrint = ""
            print ingredient.getIngredientName().ljust(15),

            for store in storeNames:
                ingredientPrice = ingredient.getPriceForRecipe(store)
                if (ingredientPrice == "unknown"):
                    toPrint += "| " + ingredientPrice.center(12) #str(ingredient.getAmountForRecipe()
                    storePriceAsterisks[storeNames.index(store)] = "*"
                else:
                    toPrint += "| "+ str(ingredient.getAmountForRecipe()) +" @"
                    toPrint += "%.2f/%s ".rjust(11) %(ingredientPrice, ingredient.getUnitStringAtStore(store))
                    pricePerStore[storeNames.index(store)] += ingredientPrice
            print toPrint      

        #border row
        print "="*16,
        for i in range(len(storeNames)):
            print "="*16, 
        print ""

        #print the total price at each store, also find the minimum asterisk and non-asterisk star
        minPrice = 100000
        minAstPrice = 100000
        print "Total Price: ".ljust(16),
        for store in storeNames:
            i = storeNames.index(store)
            toPrint = "%.2f" %pricePerStore[i]
            print (toPrint + storePriceAsterisks[i]).rjust(15),
            if storePriceAsterisks[i] == "*":
                if pricePerStore[i] < minAstPrice:
                    minAstPrice = pricePerStore[i]
                    minAstStore = store
            else:
                if pricePerStore[i] < minPrice:
                    minPrice = pricePerStore[i]
                    minPriceStore = store
        print
        print
        print "Minimum price with all ingredient prices known:", minPrice, "@",minPriceStore
        print "MinimumPrice with unknowns:", minAstPrice, "@", minAstPrice
        print
        print " "*45 + " * = price unknown for at least 1 ingredient"

    """
    print out the price of each ingredient?
    then in the actual tables print out the price of the ingredient for the recipe?
    """

    ## same as above but returns the tables to be
    # added to GUI elements
    def getPriceListFormatted(self):
        ## find all the stores where you can buy ingredients for this recipe
        storeNames = self.allPossibleStores()

        priceListString = ""

        # prepare tallies
        pricePerStore = []
        storePriceAsterisks = []
        for store in storeNames:
            pricePerStore.append(0)
            storePriceAsterisks.append(" ")

        #print store names
        priceListString = priceListString +" "*16
        for i in range(len(storeNames)):
            toPrint = "|" + storeNames[i].center(16)
            priceListString += toPrint


        #border row
        priceListString += "\n"
        priceListString += "="*16 + " "
        for i in range(len(storeNames)):
            priceListString += "="*16 + " "
        priceListString += "\n"

        #print each ingredient, and all the prices for that ingredient
        for ingredient in self.ingredientList:
            toPrint = ""
            priceListString += ingredient.getIngredientName().ljust(16)
            for store in storeNames:
                ingredientPrice = ingredient.getPriceAtStore(store)
                if (ingredientPrice == "unknown"):
                    toPrint += "| " + ingredientPrice.center(12) #+ str(ingredient.getAmountForRecipe()) +" @"
                    storePriceAsterisks[storeNames.index(store)] = "*"
                else:
                    toPrint += "| "+ str(ingredient.getAmountForRecipe()) +" @"
                    toPrint += "%.2f/%s ".rjust(11) %(ingredientPrice, ingredient.getUnitStringAtStore(store))
                    pricePerStore[storeNames.index(store)] += ingredientPrice
            priceListString += toPrint + "\n"   

        #border row
        priceListString += "="*16 + " "
        for i in range(len(storeNames)):
            priceListString += "="*16 + " "
        priceListString += "\n"

        #print the total price and find the minimum prices
        minPrice = 100000
        minAstPrice = 100000
        priceListString += "Total Price: ".ljust(16)
        for store in storeNames:
            i = storeNames.index(store)
            toPrint = "%.2f" %pricePerStore[i]
            priceListString += (toPrint + storePriceAsterisks[i]).rjust(16)
            if storePriceAsterisks[i] == "*":
                if pricePerStore[i] < minAstPrice:
                    minAstPrice = pricePerStore[i]
                    minAstStore = store
            else:
                if pricePerStore[i] < minPrice:
                    minPrice = pricePerStore[i]
                    minPriceStore = store
        priceListString += "\n"
        priceListString += "\n"
        priceListString += "Minimum price with all ingredient prices known: " + str(minPrice)+ "  @ " + str(minPriceStore) +"\n"
        priceListString += "MinimumPrice with unknowns: "+  str(minAstPrice)+ "  @ "+ str(minAstPrice)+"\n"
        priceListString += "\n"
        priceListString += " "*45 + " * = price unknown for at least 1 ingredient\n"
        

        return priceListString

    # go through and compile a string of each (groceryItem, quantity, unitPrice)
    # at each store
    def printLowestCost(self):
        storeNames = self.allPossibleStores()
        
        #prepare the tallies
        pricePerStore = []
        storePriceAsterisks = []
        
        for store in storeNames:
            pricePerStore.append(0)
            storePriceAsterisks.append(" ")

        # print each store
        print " "*15,
        for i in range(len(storeNames)):
            toPrint = "|" + storeNames[i].center(15)
            print toPrint,

        # border row
        print ""
        print "="*16,
        for i in range(len(storeNames)):
            print "="*16, 
        print ""

        # print each ingredient and the price at each store
        for ingredient in self.ingredientList:
            toPrint = ""
            print ingredient.getIngredientName().ljust(15),

            for store in storeNames:
                ingredientPrice = ingredient.getPriceForRecipe(store)
                if (ingredientPrice == "unknown"):
                    toPrint += "| " + ingredientPrice.center(12) #str(ingredient.getAmountForRecipe()
                    storePriceAsterisks[storeNames.index(store)] = "*"
                else:
                    toPrint += "| "+ str(ingredient.getAmountForRecipe()) +" @"
                    toPrint += "%.2f/%s ".rjust(11) %(ingredientPrice, ingredient.getUnitStringAtStore(store))
                    pricePerStore[storeNames.index(store)] += ingredientPrice
            print toPrint      

        #border row
        print "="*16,
        for i in range(len(storeNames)):
            print "="*16, 
        print ""

        #print the total price at each store, also find the minimum asterisk and non-asterisk star
        minPrice = 100000
        minAstPrice = 100000
        print "Total Price: ".ljust(16),
        for store in storeNames:
            i = storeNames.index(store)
            toPrint = "%.2f" %pricePerStore[i]
            print (toPrint + storePriceAsterisks[i]).rjust(15),
            if storePriceAsterisks[i] == "*":
                if pricePerStore[i] < minAstPrice:
                    minAstPrice = pricePerStore[i]
                    minAstStore = store
            else:
                if pricePerStore[i] < minPrice:
                    minPrice = pricePerStore[i]
                    minPriceStore = store

    def allPossibleStores(self):
        storeNames = []
        
        ## look through each ingredient, create a list of all the stores
        # then go through each ingredient again and print the prices out one by one
        for ingredient in self.ingredientList:
            priceList = ingredient.getPriceList()
            for price in priceList:
                if (not (price.getStoreName() in storeNames)):
                    storeNames.append(price.getStoreName())

        return storeNames


