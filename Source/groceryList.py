#! /usr/bin/env python

from ingredient import Ingredient
from recipe import Recipe

class GroceryList(object):

    ## need to add a way to remove a recipe from the grocery list

    def __init__(self):
        self.groceryList = []

    def addIngredient(self, ingredient, add):
        found = False
        newItemName = ingredient.getName()
        for masterItem in self.groceryList:
            if (newItemName == masterItem.getName()):
                if add:
                    masterItem.addAmount(ingredient.getAmount())
                else:
                    masterItem.removeAmount(ingredient.getAmount())
                found = True
                break;
    
        if not found and add:
            self.groceryList.append(ingredient.copy())

    def addIngredientList(self, ingredientList):
        if isinstance(ingredientList, Ingredient):
            self.addIngredient(ingredientList, True)
        else:
            for ingredient in ingredientList:
                self.addIngredient(ingredient, True)

    def addRecipeList(self, recipeList):
        if len(recipeList) == 1:
            self.addRecipe(recipeList[0])
        else:
            for recipe in recipeList:
                self.addRecipe(recipe)
    
    def addRecipe(self, newRecipe):
        for newItem in newRecipe.getIngredientList():
            self.addIngredient(newItem, True)

    def removeRecipeList(self, recipeList):
        if isinstance(recipeList, Ingredient):
            self.removeRecipe(recipeList)
        else:
            for recipe in recipeList:
                self.removeRecipe(recipe)

    def removeRecipe(self, r):
        for newItem in r.getIngredientList():
            self.addIngredient(newItem, False)
            
    def listToString(self):
        self.removeZeros()
        s = ""
        for item in self.groceryList:
            s += item.getFullName()

        return s
    
    def getAllIngredients(self):
        self.removeZeros()
        return self.groceryList

    def removeZeros(self):
        toRemove = []
        for item in self.groceryList:
            if item.getAmount() == 0:
                toRemove.append(item)

        for item in toRemove:
            self.groceryList.remove(item)

    def empty(self):
        self.groceryList = []

"""
    def groceryListFromRecipes(self, recipeList):
        if not recipeList:
            return
        elif len(recipeList) == 1:
            self.addRecipe(recipeList[0])
        else:
            allItems = []

            for recipe in recipeList:
                newItems = []
                ingredientList = recipe.getIngredientList()
                for ingredient in ingredientList:
                    newItems.append(ingredient.copy())

                self.addItemsToList(allItems, newItems)            
        
            return allItems



    def combineDoubleIngredients(self, ingredientList):
        newIngredientList = []
        repeats = []

        while (not ingredientList):
            anItem = ingredientList.pop()
            ingredientName = anItem.getIngredientName()
            for i,ingredient in enumerate(ingredientList):
                if (ingredientName == ingredient.getIngredientName()):
                    repeats.append(i)

            for i in repeats:
                repeatItem = ingredientList.pop(i)
                anItem.addAmount(repeatItem.getAmount)

            newIngredientList.append(anItem)

        return newIngredientList
"""
