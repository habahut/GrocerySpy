#! /usr/bin/env/ python

"""
stores the price and store this price can be found at

also retains the quantity
"""

class Price(object):

    def __init__(self, c,a, uS, s):
        self.cost = c
        self.storeName = s

        # grams, liters, etc... translated to "per" for something like donuts
        # that are individually purchased
        #
        # strip "s" from the end of the unitString, if it is there
        uS = uS.lower()
        if (uS != "lbs"):
            l = len(uS)
            if (uS[l-1:l] == "s"):
                uS = uS[:l-1]
        
        self.unitString = uS.lower()
        # how many grams liters?
        self.amount = a

    # returns the price per one unit of the item and the unitString
    def getUnitPrice(self):
        return str(self.cost/self.amount) + " " +self.unitString

    # just returns the price number
    def getPriceNumber(self):
        return self.cost

    #just returns the "units" string for this price
    def getPriceUnits(self):
        return self.unitString

    def getStoreName(self):
        return self.storeName

    def getAmount(self):
        return self.amount


class RecipePrice(Price):

    def __init__(self, c, a, uS, s, rN):
        super.__init__(c, a, uS, s)
        self.recipeName = rN

    def getRecipeName(self):
        return self.recipeName
