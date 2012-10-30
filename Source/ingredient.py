#! usr/bin/env python

"""
an individual item, part of a recipe
a wrapper for a grocery object, keeps the quantity here

stores quantity in memory
scaling of the recipe will change the data in the object but not the
persistent data in the file. Calling writeToFile() will permenantly
change the file on this recipe

within this object we store the price of the item for the recipe it is a part of
that way scaling is more simple
"""

class Ingredient(object):
    ## i should eventually go through and just delete the groceryItem and Price classes
    # there is no need for them now that I am not doing the price comparisons
    def __init__(self, n, a, uS, m = ""):
        self.name = n
        self.amount = float(a)
        self.unitString = uS.lower()
        # the unit string here is the units on the recipe, not the price
        self.modifier = m


    ## this is from the dictionary, so we know the form it takes
    @classmethod
    def fromString(cls, s):
        if not s == "":
            #print "recievied: ", s
            name, units = s.split(":")
            #print "     name: ", name, "units: ", units
            modifiers = ""
            if (not(name.find(",") == -1)):
                name,modifiers = name.split(",")
                name = name.rstrip().lstrip()
                modifiers = modifiers.rstrip().lstrip()
                

            temp = units.split()
            if len(temp) == 1:
                amount = units
                unitString = name
            else:
                amount = temp[0]
                unitString = ""
                for i in range(1, len(temp)):
                    unitString += temp[i] + " "

            """elif len(temp) == 2:
                amount = temp[0]
                unitString = temp[1]
            else:
                ## too many values
                # good assumption to make: first is amount, last is unitString
                amount = temp[0]
                unitString = temp[len(temp) - 1]
                print "unitString is: ", unitString
                #raise ValueError("in ingredient.fromString, units = " + units + ". Too many values")"""
            
            return cls(name, amount, unitString, modifiers)
        else:
            return None

    def getName(self):
        return self.name

    def getModifier(self):
        return self.modifier

    def getFullName(self):
        if self.modifier == "":
            return self.name +": "+ str(self.amount) + " " + self.unitString
        else:
            return self.name +", "+self.modifier+": "+ str(self.amount) + " " + self.unitString
        

    def toString(self):
        return self.getFullName()

    def getReadableName(self):
        readableName = str(self.amount)
        if self.unitString != self.name:
            readableName += " " + self.unitString
        readableName += " " + self.name
        if self.modifier != "":
            readableName += ", " + self.modifier
        return readableName

    def scale(self, d):
        self.amount /= d

    def getAmountForRecipe(self):
        return self.amount

    def getUnitString(self):
        return self.unitString

    def getAmount(self):
        return self.amount
    
    def addAmount(self, na):
        self.amount += na

    def removeAmount(self, na):
        self.amount -= na

    ## returns a copy of the ingredient argument
    def copy(self):
        return Ingredient(self.name, self.amount, self.unitString)


    """
=-----------------------=-==--=-==--=-=-=-=-=-==--==-=-=-=--=-=-==--==-=-=-=--=-=
-==--==-=-=-=--=-=-==--==-=-=-=--=-=-==--==-=-=-=--=-=-==--==-=-=-=--=-=-==--==-=-=-=--=-=
-==--==-=-=-=--=-=-==--==-=-=-=--=-=-==--==-=-=-=--=-=-==--==-=-=-=--=-=-==--==-=-=-=--=-=
-==--==-=-=-=--=-=-==--==-=-=-=--=-=-==--==-=-=-=--=-=-==--==-=-=-=--=-=-==--==-=-=-=--=-=

OLD CODE, prices 
    



    def getUnitStringAtStore(self, storeN):
        # if something is in a unit that is the thing itself i.e. bananas $.79 per banana
        # return unit as "per" to save formatting space
        if (self.groceryItem.getUnitAtStore(storeN).lower() == self.groceryItem.getName().lower()):
            return "per"
        else:
            return self.groceryItem.getUnitAtStore(storeN).lower()

  



    

    def getGroceryItem(self):
        return self.groceryItem

    # left this one in in case it was used elsewhere, dont feel like checking
    # that now
    def getQunatity(self):
        return self.amount

    
        
    # called by the database manager, when permanent changes should be made
    # to the recipe
    def toFileString(self):
        return self


    def getPriceList(self):
        return self.groceryItem.getPriceList()

    ## this needs to be switched to return the price
    # and the units together
    def getPriceAtStore(self, storeN):
        return self.groceryItem.getPriceNumberAtStore(storeN)

    ## return a tuple of all the prices and the stores, for easy formatting
    # better yet return an array ["store price", ...] use .split() to seperate
    def getAllPrices(self):
        pass

    ## returns the price of the quantity of this ingredient for the recipe
    def getPriceForRecipe(self, storeN):
        priceStringWithUnits = self.groceryItem.getUnitPriceAtStore(storeN)

        if priceStringWithUnits == "unknown":
            return "unknown"
        else:
            price,unitString = priceStringWithUnits.split(" ")
            price = float(price)
            
            if unitString == self.unitString:
                return price * self.amount
            #else convert, not implemented yet

    """
            
