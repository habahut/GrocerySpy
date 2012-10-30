#! /usr/bin/env python

from ingredient import Ingredient

## these follow this form:
#       <num> |unit| {name} (, modifer)
# so we split by " ". Then we check each thing for a comma.
# if there is a comma, we now know where the modifier is.

## for now we are going to assume everything is of the form above
## i.e. the modifier will come last, and all terms after the , will
## be part of the modifier.

## as we build this up with recipes from allrecipes.com, we will
# create a database of common words that can be associated with each category
# then we can use that database to help seperate the strings.



"""
Number words currently break this program...
i.e. "one can beef broth or 2 cups water with dissolved beef bouillon**"
who the fuck enters shit by typing out the number? what a bitch...
"""



class IngredientParser(object):

    def __init__(self, parserDataFields):#, nameList, modifierList, amountList, unitStringList):
        """self.nameList = nameList
        self.modifierList = modifierList
        self.amountList = amountList
        self.unitStringList = unitStringList"""

        self.message = ""

        self.inputStringList = []
        self.currentString = 0

        self.finalIngredientList = []

        print parserDataFields
        self.preModifierList = parserDataFields["PreModifiers"]
        print self.preModifierList

    def getFinishedIngredientList(self):
        if self.message == "done":
            return self.finalIngredientList
        else:
            return "notDone"
    

    def passString(self, iS):
        iS = iS.replace("\r\n", "\n")
        self.inputStringList = iS.split("\n")

    ## this handles calls for the ingredientParser to 'parse'
    # its given block of text
    def parse(self):
        result = ""
        for i in range(self.currentString, len(self.inputStringList)):
            result = self.doParse(self.inputStringList[i])
            if isinstance(result, Ingredient):
                ## no errors, append this to the finalIngredientList
                self.finalIngredientList.append(result.toString())
            elif isinstance(result, str):
                ## returned a string, meaning there is confusion parsing the
                # string,
                """
                not implemented yet!!!
                will ask the user for clarification regarding this specific
                ingredient
                """
                self.message = result
                return result

        ## if it has gotten here than no confusion has occured, simply return
        # "done" to let program know final list is ready
        self.message = "done"
        return "done"
        

    def doParse(self, thisString):
        print
        print
        print "working on: ", thisString
        
        stringList = thisString.split()
        print "num terms: ", len(stringList)
        print
        print

        if (len(stringList) == 0):
            ## sometimes a blank line will come through
            # so just return and wait for the next one
            return None
        
        amount = 0
        unitString = ""
        name = ""
        modifiers = ""
        done = False        

        # the format <#> <# ounce can of ____> currently breaks the program
        # so we need to have a custom thing to detect that
        if not (thisString.lower().find(" can ") == -1):
            amount = self.parseAmount(stringList[0])
            for i in range(1, len(stringList)):
                name += stringList[i] + " "
            unitString = name

            return Ingredient(name, amount, unitString, modifiers)

        ## we first check some things about the stringList to try and
        # guess the format it is in
        if (not (thisString.find(",") == -1)):
            tempList = thisString.split(",")
            beforeCommaList = tempList[0].split()
            afterCommaList = tempList[1].split()

            ## i.e.: "2 jalapenos, seeded and minced"
            if (len(beforeCommaList) == 2):
                amount = beforeCommaList[0]
                name = beforeCommaList[1]
                unitString = name
                for s in afterCommaList:
                    modifiers += s + " "

                return Ingredient(name, amount, unitString, modifiers)                
                
        if (len(stringList) == 2):
            # the length is only two, so it must be something like
            # "2 eggs," in which case the unit is the name and modifiers is blank
            # it could be reverse ordered thought "eggs 2" or something...
            if (stringList[0][0] == "." or stringList[0][0].isdigit()):
                ## the first part is a number so it is probably of the "2 eggs" variety
                amount = self.handleHyphenatedAmount(stringList[0])
                name = stringList[1]
                # units will be teh same as name here
                unitString = name
            else:
                ## the order is probably reversed, so "eggs: 2"
                # or something like that
                ## should ask alec for a regex that removes non-alphabetic characters
                name = stringList[0]
                unitString = name
                amount = self.handleHyphenatedAmount(stringList[1])
            done = True    

        elif (stringList[0][0] == "." or stringList[0][0].isdigit()):
            ## the first digit is a number
    
            # stringList[0] is a number, which means it is an amount
            # so we want to start on the second index of stringList
            counter = 1
           

            # in this case we will guess that it is of the form
            # <num> |unit| {name} (, modifer)
            # i.e.: 3 teaspoons sugar, granulated
            amount += self.parseAmount(stringList[0])


            ## 3 possible options from here, a # - # meaning a range seperated by spaces
            if (stringList[1] == "-"):
                if (stringList[2][0] == "." or stringList[2][0].isdigit()):
                    temp = self.parseAmount(stringList[2])
                    amount = (amount + temp)/2.00
                    counter = 3
                else:
                   raise IngredientInputError("Ingredient String Makes No Sense!")
            elif (stringList[1][0] == "." or stringList[1][0].isdigit()):
                amount += self.parseAmount(stringList[1])
                counter += 1
            
            
            ## here we should cross check with the database to confirm if our assumption
            # is correct. Checking the potential unitString against the database
            # of previous unitStrings and "connectors:" i.e. "of, ':'" etc...
            # will help determine if this ingredient string is of the type we guessed

            #!!! here we need to also check if this word is something to do with the name
            # of the ingredient. For example "green peppers" or "large onions." in either
            # case green or large would fall into the "unit string" field.
            unitString, modifiers, counter = self.considerUnitString(stringList, counter)            

            ## since we have now assumed we have grabbed the above values correctly
            # everything from here to the end of the string, or from here to a comma
            # is part of the name of the ingredient
            hasModifier = False
            for i in range(counter, (len(stringList))):
                if (not (stringList[i].find("(") == -1)):
                    hasModifier = True
                    break
                name += stringList[i]
                print "name is: ", name, " i @ ", i, "   len: ", len(stringList)
                if (not (name.find(",") == -1)):
                    # the string we just added contains a comma, meaning
                    # this ingredient has a modifier
                    name = name.strip(",")
                    i += 1
                    hasModifier = True
                    break
                else:
                    name += " "
            name = name.rstrip()

            print
            print
            print "length of stringList = ", len(stringList)
            print
            print
            
            if (hasModifier):
                for i2 in range(i, len(stringList)):
                    modifiers += stringList[i2].strip(",").strip("(").strip(")")+ " "
                    print "modifiers: ", modifiers
        
            if unitString == "":
                unitString = name

        print "name: ", name
        print "modifiers: ", modifiers
        print "amount: ", amount
        print "unitString: ", unitString
        
        # we want this to be in string form in the dictionary:
        # i.e.: name?(,modifiers): amount unitString
        # but we need to make it an ingredient for now so we can differentiate
        # between finished products and error messages
        return Ingredient(name, amount, unitString, modifiers)

    def parseAmount(self, stringList):        
        amountList = stringList.split("-")
        blankElements = []
        for i in range(len(amountList)):
            if amountList[i] == "":
                blankElements.append(i)
            else:
                amountList[i] = self.handleFractionalAmount(amountList[i])

        for i in blankElements:
            amountList.pop(i)
        
        if (len(amountList) == 1):
            return amountList[0]
        else:
            return (amountList[0] + amountList[1])/2.00

    def handleFractionalAmount(self, string):
        s = string.split("/")
        if (len(s) == 1):
            ## i.e. no fraction
            print "s[0] is : ", s[0]
            return float(s[0])
        else:
            return float(s[0])/float(s[1])

    def considerUnitString(self, stringList, startIndex):
        modS = ""
        unitString = ""

        done = False
        while not done:
            done = True
            if (not (stringList[startIndex].find("(") == -1)):                
                if (not (stringList[startIndex].find(")") == -1)):
                    modS += stringList[startIndex].strip("(").strip(")") + " "
                    startIndex += 1
                else:
                    modS += stringList[startIndex].strip("(") + " "
                    startIndex += 1
                    while (not (stringList[startIndex].find(")") == -1)):
                        modS += stringList[startIndex].strip(")") + " "
                        startIndex += 1
                    
            for word in self.preModifierList:
                if stringList[startIndex].strip(",").lower() == word.lower():
                    modS += stringList[startIndex].strip(",") + " "
                    startIndex += 1
                    done = False
                    break
                
                    

        if modS == "":
            unitString = stringList[startIndex].strip(",")
            startIndex += 1

        print "after consideration:  unitString:", unitString, "  modS: ", modS, " startIndex: ", startIndex
        return unitString,modS,startIndex 
                
                


class IngredientInputError(Exception):
    def __init__(self, v):
        self.val = v
    def __str__str(self):
        return repr(self.val)
    

if __name__ == "__main__":
    parser = IngredientParser({"PreModifiers": ["delicious","sweet","green", "red", "orange", "blue", "spicy", "large", "chopped", "big", "medium", "sized"]})
    #parser = IngredientParser(["large","green"])
    datString = raw_input("try me: ")
    parser.passString(datString)
    print "returned",  parser.parse()
    print "==========="    
    #print parser.considerUnitString(datString.split(), 1)
    print
    print
    print "final ingredient List: " , parser.getFinishedIngredientList()


"""
4 medium sized potatoes (peeled/chunked)
3 carrots (sliced)
1 sweet (bell) green pepper (chunked)
1 medium sized yellow onion (chopped)
1/4 head of green cabbage (shredded)
1-2 stalks of celery (sliced 1/4-1/2")
1 red delicious apple (peeled/chunked)
1 small turnip (chunked)
1- 14 oz can whole kernel corn (drained)
1- 14oz can green peas (drained)
64 oz V8 (or other brand) 100% vegetable juice
1.5 lb. beef chuck roast
one can beef broth or 2 cups water with dissolved beef bouillon**
1 tsp dried basil
1 tsp. oregano
"""











        


             
