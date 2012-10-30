#! /usr/bin/env python

from ingredient import Ingredient
import re
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


class IngredientParser(object):

    def __init__(self):#, parserDataFields):#, nameList, modifierList, amountList, unitStringList):

        self.numberWords = {'sixty-one': 61.0, 'seventy-two': 72.0, 'thirty one': 31.0, 'fifty-one': 51.0, 'seventy nine': 79.0, 'sixty-two': 62.0, 'fifty': 50.0, 'four': 4.0, 'forty-six': 46.0, 'twenty-three': 23.0, 'ninety six': 96.0, 'eighty one': 81.0, 'seventy-seven': 77.0, 'fifty six': 56.0, 'sixty two': 62.0, 'twenty two': 22.0, 'eighty-four': 84.0, 'forty eight': 48.0, 'fifty four': 54.0, 'ninety eight': 98.0, 'seventy five': 75.0, 'ninety five': 95.0, 'seventy-five': 75.0, 'forty-nine': 49.0, 'seventy three': 73.0, 'five': 5.0, 'twenty five': 25.0, 'half': 0.5, 'sixteen': 16.0, 'forty-five': 45.0, 'sixty-nine': 69.0, 'eighty six': 86.0, 'fifty seven': 57.0, 'twenty nine': 29.0, 'sixty four': 64.0, 'forty-four': 44.0, 'fifty-six': 56.0, 'twenty six': 26.0, 'ninety-two': 92.0, 'thirty-eight': 38.0, 'quarter': 0.25, 'forty one': 41.0, 'sixty-five': 65.0, 'twelve': 12.0, 'seventeen': 17.0, 'fifty three': 53.0, 'ten': 10.0, 'ninety one': 91.0, 'sixty three': 63.0, 'thirty seven': 37.0, 'ninety nine': 99.0, 'thirteen': 13.0, 'thirty six': 36.0, 'thirty two': 32.0, 'seventy-four': 74.0, 'ninety-one': 91.0, 'forty': 40.0, 'forty five': 45.0, 'forty-three': 43.0, 'seventy six': 76.0, 'twenty-five': 25.0, 'eighty four': 84.0, 'sixty-eight': 68.0, 'seventy-eight': 78.0, 'eighty three': 83.0, 'forty four': 44.0, 'ninety-nine': 99.0, 'forty-seven': 47.0, 'ninety-three': 93.0, 'sixty nine': 69.0, 'fourteen': 14.0, 'forty seven': 47.0, 'fifty-seven': 57.0, 'sixty': 60.0, 'fifteen': 15.0, 'seventy': 70.0, 'fifty one': 51.0, 'sixty seven': 67.0, 'thirty': 30.0, 'twenty-seven': 27.0, 'seventy-three': 73.0, 'fifty-four': 54.0, 'eighty eight': 88.0, 'forty six': 46.0, 'thirty nine': 39.0, 'sixty-three': 63.0, 'twenty-six': 26.0, 'twenty-two': 22.0, 'seventy-six': 76.0, 'ninety two': 92.0, 'sixty-six': 66.0, 'thirty-one': 31.0, 'one': 1.0, 'eighty-seven': 87.0, 'ninety': 90.0, 'forty two': 42.0, 'fifty nine': 59.0, 'seventy-one': 71.0, 'ninety seven': 97.0, 'thirty five': 35.0, 'fifty-three': 53.0, 'seventy-nine': 79.0, 'twenty': 20.0, 'sixty-seven': 67.0, 'two': 2.0, 'eighth': 0.125, 'seventy seven': 77.0, 'eleven': 11.0, 'ninety four': 94.0, 'eighty-two': 82.0, 'twenty seven': 27.0, 'twenty-eight': 28.0, 'seventy one': 71.0, 'eighty-one': 81.0, 'seventy eight': 78.0, 'ninety-seven': 97.0, 'nineteen': 19.0, 'eighty nine': 89.0, 'eighty-three': 83.0, 'twenty-one': 21.0, 'forty three': 43.0, 'fifty five': 55.0, 'twenty one': 21.0, 'sixty six': 66.0, 'fifty two': 52.0, 'nine': 9.0, 'three': 3.0, 'thirty-five': 35.0, 'sixty one': 61.0, 'twenty-four': 24.0, 'ninety-six': 96.0, 'fifty-nine': 59.0, 'seven': 7.0, 'seventy two': 72.0, 'thirty-nine': 39.0, 'sixty-four': 64.0, 'sixty eight': 68.0, 'forty nine': 49.0, 'eighteen': 18.0, 'fifty-eight': 58.0, 'ninety-five': 95.0, 'thirty-three': 33.0, 'thirty four': 34.0, 'eighty seven': 87.0, 'ninety three': 93.0, 'six': 6.0, 'fifty-five': 55.0, 'eighty two': 82.0, 'fifty eight': 58.0, 'forty-one': 41.0, 'eighty-six': 86.0, 'eight': 8.0, 'ninety-eight': 98.0, 'twenty four': 24.0, 'eighty': 80.0, 'thirty-six': 36.0, 'thirty-two': 32.0, 'eighty-eight': 88.0, 'thirty-seven': 37.0, 'eighty-nine': 89.0, 'ninety-four': 94.0, 'thirty three': 33.0, 'twenty eight': 28.0, 'twenty-nine': 29.0, 'thirty eight': 38.0, 'eighty five': 85.0, 'seventy four': 74.0, 'forty-two': 42.0, 'forty-eight': 48.0, 'thirty-four': 34.0, 'sixty five': 65.0, 'eighty-five': 85.0, 'fifty-two': 52.0, 'twenty three': 23.0}
        
        self.preModifiers = {"medium-sized","black", "delicious","sweet","green", "red", "orange", "blue", "spicy", "large", "chopped", "big", "medium", "sized"}

        ## extra shit that people put in the names of ingredients: like "1.5 liters <of> water"
        self.pointlessWords = ["of","a"]
        self.abbreviatedUnitStrings = {"g":"grams",
                          "tbsp":"tablespoons",
                          "tablespoon":"tablespoons",
                          "tsp":"teaspoons",
                          "teaspoon":"teaspoons",
                          "kg":"kilograms",
                          "kilogram":"kilograms",
                          "oz":"ounce"}

        self.message = ""

        self.inputStringList = []
        self.currentString = 0

        self.finalIngredientList = []

        #self.preModifierList = parserDataFields["PreModifiers"]

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
        #print
        #print
        #print self.inputStringList
        #print self.currentString
        for i in range(self.currentString, len(self.inputStringList)):
            # sometimes blank lines get entered, need to filter those out
            if (self.inputStringList[i] == ""):
                continue
            #print "parsing: ", self.inputStringList[i]
            result = self.doParse(self.inputStringList[i])
            #print "result: ", result
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
        


    ## determines if the value is of the form
    #   <#>"unitString" (one word) or is just a number
    #   splits it if it is 
    def splitByNum(self, string):
        #print "got ", string

        # first check for decimals
        regex = re.compile("^\d+\.*\d*|^\d*\.\d+")
        m = regex.match(string)
        if m == None:
            #print "looking for fractions in ", string
            # check for fractions before giving up
            regex = re.compile("^\d+\s?/\s?\d+")
            m = regex.match(string)

            # stil nothing... give up
            if m == None:                 
                return False, [string, '']
            
        #print "true"
        #print m.group()
    
        nums = [m.span()[0],m.span()[1]]
        letters = [m.span()[1],len(string)]

        return True,[nums,letters]

    ## if the string contains no discernable numbers we treat it as "oil for cooking or something"
    # this determines if htat is the case or if we can proceed to process the string
    # returns True if string can be processed:
    #           [amount, unitString]   <-- will only return a value for unitString if it is originally
    #                                       one word, i.e. "500g"
    # returns False if the string cannot be further processed
    def tryParseNum(self, string):
        amount = 0
        unitString = ""    
        #print "recieved :", string

        isDone,indexList = self.splitByNum(string)
    
        tempList = []
        # templist[0] is the part of the string that is a number
        tempList.append(string[indexList[0][0]:indexList[0][1]])
        # tempList[1] is the unitString
        tempList.append(string[indexList[1][0]:indexList[1][1]])
        #print "got back: ", isDone, "  ", tempList
        #print
        if isDone:
            # of the form <#>"unitString" or just <#>
            amount = float(tempList[0])
            if not tempList[1] == "":                
                unitString = self.abbreviatedUnitStrings[tempList[1]]
            return True,[amount,unitString]
        else:
            #print "got here"
            # not of that form
            # check if it is a number first
            if tempList[0] in numberWords.keys():
                amount = self.numberWords[tempList[0]]
                return True,[amount]
            else:
                # there are no numbers, don't know how to parse this thing so we return false
                # hopefully this is because it is of the form "oil for cooking" or somehting like that
                return False, []

    ## this presumes the list is split already
    ## will look through to match the following
    ## returns False if no hyphen is present
    ## otherwise will return True and modify the string to make it easier to read       
    def handleAmount(self, string):
        # scan the string and find all instances of the form:
        # number - number || number "to" number
        "old regex: "
        #regex = re.compile("\d*\s*-\s*\d*\D?|\d*\s*to\s*\d*\D?")
        #                   # - # or # to #
        "current regex: "
        regex = re.compile("\d*\s*-\s*\d*\S*|\d*\s*to\s*\d*\S*")

        "new regex (to include fractions)"
        #first part # <spaces?> /(fraction maybe?) <spaces?> #?
        #regex = re.compile("\d*\s?\/?\s?\d?\s*-\s*\d*\s?\/?\s?\d?\S*|\d*\s*\/*\s*\d*\s*to\s*\d*\s*\/*\s*\d*\S*")
        
        m = regex.match(string)

        # more readable to do two checks, above for ranges and this one for fractions
        if m == None:
            #print "looking @ ", string
            fractionsWithHyphen = "\d+\s?/\s?\d+\s*-*\s*\d+\s?/*\s?\d+\s*\S*"
            fractionsWithTo = "\d+\s?/\s?\d+\s*to*\s*\d+\s?/*\s?\d+\s*\S*"
            regex = re.compile(fractionsWithTo)# +"|" +fractionsWithHyphen )
            
            m = regex.match(string)
            #if not m==None:
            #print "found", string[m.span()[0]:m.span()[1]]

        """ the current state of things:
        this is not finding the right things, its grabbing the entire word after
        the fraction section

        parseByNum() has been changed to try to look for fractions... this may be redundant
        need to trace this shit a little bit

        also, it might make more sense to go through this bitch and first replace
        all number words with the corresponding numbers... might make things simpler later
        """
        
        if m == None:
            #no ranges of values, so we look through each element to find the number
            # first we search for fractions:

            """
            fraction regex here!
            """


            
            found = False
            stringList = string.split()        
            for s in stringList:
                #print "all day: ",s
                # examine each word in the ingredient string, see if we can
                # find a number
                foundNum,indexList = self.splitByNum(s)
                if foundNum:
                    found = True
                    break
                else:
                    # wasn't in digit form, check for word form
                    if s.lower() in self.numberWords.keys():
                        # remove the number word from the string
                        # and return the values
                        #print "got to here!"
                        found = True
                        stringList.pop(stringList.index(s))
                        newString = ""
                        for w in stringList:
                            newString += w + " "
                        return True,newString, self.numberWords[s.lower()],""
                                            
            if not found:
                #no numbers
                return False, string, "", ""
            else:                                   
                unitString = string[indexList[1][0]:indexList[1][1]]
                amount = string[indexList[0][0]:indexList[0][1]]
                #print "amount found to be ", amount
                #print "unitString found to be ", unitString
                return True, self.cutUpString(string,indexList[0][0],indexList[1][1]), amount, unitString
        else:
            ## isolate each number    
            theNumbers = string[m.span()[0]:m.span()[1]]
    
            ## hacky solution... since we don't know where there was a
            # hyphen or "to" denoting the range, we must check both options
            n = theNumbers.split("-")
            if (len(n) == 1):
                n = theNumbers.split(" to ")
            n[0] = n[0].lstrip().rstrip()
            n[1] = n[1].lstrip().rstrip()
    
            string = self.cutUpString(string,m.span()[0],m.span()[1]).rstrip().lstrip()
            #print "here you go!:", string

            isParseAble1,result1 = self.tryParseNum(n[0])
            #print "first:", isParseAble1, "  ", result1        
            isParseAble2,result2 = self.tryParseNum(n[1])
            #print "segundo:", isParseAble2, "  ", result2

            if isParseAble1 and isParseAble2:
                #print "result 1:", result1
                #print "result 2:", result2
                avg = (float(result1[0]) + float(result2[0]))/2.0
                return True,string, avg,result2[1]                
            else:
                pass                
                # throw an error here for handling back in the main program
    
    def handleUnitString(self, string):
        initialString = string
        stringList = string.split()
        removalS = []
    
        modS = ""
        unitString = ""
        startIndex = 0
    
        done = False
        while not done:
            done = True
            if (not (stringList[startIndex].find("(") == -1)):                
                if (not (stringList[startIndex].find(")") == -1)):
                    modS += stringList[startIndex].strip("(").strip(")") + " "
                    removalS.append(startIndex)
                    startIndex += 1
                else:
                    modS += stringList[startIndex].strip("(") + " "
                    startIndex += 1
                    while (not (stringList[startIndex].find(")") == -1)):
                        modS += stringList[startIndex].strip(")") + " "
                        removalS.append(startIndex)
                        startIndex += 1
                    
            for word in self.preModifiers:
                if stringList[startIndex].strip(",").lower() == word.lower():
                    modS += stringList[startIndex].strip(",") + " "
                    removalS.append(startIndex)
                    startIndex += 1
                    done = False
                    break
                    
        if modS == "":
            unitString = stringList[startIndex].strip(",")
            removalS.append(startIndex)
            startIndex += 1
    
        for n in reversed(removalS):
            stringList.pop(n)
    
        s = ""
        for i in range(len(stringList)):
            s += stringList[i] + " "

        #print "after consideration:  unitString:", unitString, "  modS: ", modS, " startIndex: ", startIndex
        return True,s,unitString,modS

    def handleNameModifier(self, stringList):
        ## since we have now assumed we have grabbed the above values correctly
        # everything from here to the end of the string, or from here to a comma
        # is part of the name of the ingredient
        name = ""
        modifiers = ""
        hasModifier = False
        for i in range(0, (len(stringList))):
            if (not (stringList[i].find("(") == -1)):
                hasModifier = True
                break
            name += stringList[i]
            #print "name is: ", name, " i @ ", i, "   len: ", len(stringList)
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
    
        """print
        print
        print "length of stringList = ", len(stringList)
        print
        print"""
            
        if (hasModifier):
            for i2 in range(i, len(stringList)):
                modifiers += stringList[i2].strip(",").strip("(").strip(")")+ " "
                #print "modifiers: ", modifiers

        return name,modifiers

    def cutUpString(self, string, start, end):
        p1 = string[0:start]
        p2 = string[end:len(string)]
        return p1 + p2
    
    def removePointlessWords(self, string):
        for w in self.pointlessWords:
            #regex = re.compile("^\s*"+w+"\s")
            #print "checking: ", w
            string = self._removePointlessWords(string, w)
    
        return string
    
    def _removePointlessWords(self, string, regex):
        newString = ""
        for s in string.split():
            #m = regex.match(s)
            if not s.lower() == regex:
                #print "     didn't find in: ", s
                newString += s + " "

                #if not m == None:            
                #    name = cutUpString(name,m.span()[0],m.span()[1])
        return newString

    def insertWord(self, string, word, index):
        stringList = string.split()
        newStringList = []
        for i in range(0, index):
            newStringList.append(stringList[i])

        newStringList.append(word)
        for i in range(index,len(stringList)):
            newStringList.append(stringList[i])

        newString = ""
        for w in newStringList:
            newString += w + " "
    
        return newString                            

    def doParse(self, string):
        initialString = string
        string = self.removePointlessWords(string)
        amount = 0
        name = ""
        modifiers = ""

        #print "         string is :", string
    
        cont,string,amount,unitString = self.handleAmount(string)
        if not cont:
            #print "could not parse, name = ", initialString
            ## this needs to actually create an ingredient, set amount = 1
            return initialString
        if unitString == "":
            #print "got to this point"
            cont,string,unitString,modifiers = self.handleUnitString(string)
            #print "         string is :", string       
            
        ## check how many terms are left in the string
        stringList = string.split()
        if len(stringList) == 0:
            #print "here"
            # empty, means the name = unitString
            name = unitString
        elif len(stringList) == 1:
            #only one thing left in the string, it must be the name
            #print "there"
            name = stringList[0]
            #return name,modifiers,amount,unitString
        else:
            #print "aqui"
            name,modifier = self.handleNameModifier(string.split())
            
        unitString = unitString.lower()
        name = name.lower()
        modifiers = modifiers.lower()

        # some common cases where this thing goes wrong
        if unitString == "":
            unitString = name
        elif unitString == "can":
            name = self.insertWord(name, "can", 0)
            unitString = name
        elif unitString in self.abbreviatedUnitStrings.keys():
            unitString = self.abbreviatedUnitStrings[unitString]
        elif not (unitString.find("(")):
            # unitString should not have parenthesis, that means
            # the name is probably here
            pass
    
       
        """print "thus far:"
        print "     name: ", name
        print "     modifiers: ", modifiers
        print "     amount: ", amount
        print "     unitString: ", unitString"""
        

        #return Ingredient.fromString(name +":"+ modifiers amount: " + str(amount) +"   unitString: " + unitString
        return Ingredient(name, amount, unitString, modifiers)

class IngredientInputError(Exception):
    def __init__(self, v):
        self.val = v
    def __str__str(self):
        return repr(self.val)
    



x = """
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

if __name__ == "__main__":
    parser = IngredientParser()#{"PreModifiers": ["delicious","sweet","green", "red", "orange", "blue", "spicy", "large", "chopped", "big", "medium", "sized"]})
    #parser = IngredientParser(["large","green"])
    datString = raw_input("try me: ")
    parser.passString(datString)

    #print parser.splitByNum(datString)
    #print x
    #parser.passString(x)
    print "returned"
    g = parser.parse()
    print g
    print "==========="    
    #print parser.considerUnitString(datString.split(), 1)
    print
    print
    ingList = parser.getFinishedIngredientList()
    for ing in ingList:
        print ing














        


             
