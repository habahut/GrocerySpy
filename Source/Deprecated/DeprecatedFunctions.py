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
