#! /usr/bin/env python

# MAH BALLS!!!!
"""
stores the item name
and a list of prices for each location it is at

quantity of each unit will be stored within the price


I stored stuff by GroceryItem -> Price@store, Price@store, etc..
instead of Store -> GroceryItem, GroceryItem, etc...
because I figured there would be way more items than stores. To find the price of
something using the second method (sorting info by store) we would have to
search through all the items at store A to find the price, then through
all the items in store B etc..

my way only needs to search through a few stores to find the specific price
that way there is a lot less searching and hopefully things will go faster
"""
class GroceryItem(object):

    def __init__(self, n, p, r = "unknown"):  
        self.priceList = p
        self.name = n
        self.rating = r

    def getPriceList(self):
        return self.priceList

    def findLowestPrice(self):
        minPrice = 1000

        #fucking stupid python, have to do it this way
        """
        here we need to ensure that we are using the right unit type.
        so I want to check the first element of the price list without
        removing it, and then convert all other units in the price list
        to that type. Unfortunately python doesn't have an easy way to do this
        that I can find. So we will have to hack something stupid together here

        ... should just fucking learn java graphics and do this in java...
        """
        
        #firstUnits = self.priceList.
        
        for p in self.priceList:
            if p.getPrice() < minPrice:
                minPrice = p.getUnitPrice()
                storeName = p.getStore()

        ## needs to somehow take into account the different unit prices    
        return (minPrice,storeName)
    
    def getPriceNumberAtStore(self, storeN):
        found = False
    
        for p in self.priceList:
            if p.getStoreName() == storeN:
                foundPrice = p.getPriceNumber()
                found = True

        if found:
            return foundPrice
        else:
            return "unknown"

    def getUnitAtStore(self, storeN):
        found = False
    
        for p in self.priceList:
            if p.getStoreName() == storeN:
                unitS = p.getPriceUnits()
                found = True

        if found:
            return unitS
        else:
            return "unknown"

    # returns "the price for 1 unit of the item at the given store    unitString"
    def getUnitPriceAtStore(self, storeN):
        found = False
        for priceObject in self.priceList:
            if (priceObject.getStoreName() == storeN):
                priceString = priceObject.getUnitPrice()
                found = True
                break

        # this is a string!!
        if found:
            return priceString
        else:
            return "unknown"
    
    def getName(self):
        return self.name

    def getAllCosts(self):
        return self.priceList
    
                
