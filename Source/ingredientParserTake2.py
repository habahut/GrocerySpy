#! /usr/bin/env python

import re


numberWords= {'twelve': '12', 'seven': '7', 'twenty-two': 'twelve', 'ten': '10', 'third': 'quarter', 'twenty-six': 'sixteen', 'seventeen': '17', 'two': '2', 'four': '4', 'sixty': '60', 'eighteen': '18', 'thirteen': '13', 'twenty-three': 'thirteen', 'one': '1', 'twenty-nine': 'nineteen', 'fifty': '50', 'twenty': '20', 'six': '6', 'three': '3', 'eleven': '11', 'twenty-five': 'fifteen', 'twenty-eight': 'eighteen', 'eighty': '80', 'thirty-one': '31', 'fourteen': '14', 'five': '5', 'half': '1/2', 'nineteen': '19', 'sixteen': '16', 'fifteen': '15', 'seventy': '70', 'forty': '40', 'thirty': 'twenty', 'twenty-one': 'eleven', 'twenty-seven': 'seventeen', 'ninety': '90', 'nine': '9', 'eight': '8', 'quarter': '1/4', 'twenty-four': 'fourteen'}
preModifiers = {"medium-sized","black", "delicious","sweet","green", "red", "orange", "blue", "spicy", "large", "chopped", "big", "medium", "sized"}

## extra shit that people put in the names of ingredients: like "1.5 liters <of> water"
pointlessWords = ["of","a"]
abbreviatedUnitStrings = {"g":"grams",
                          "tbsp":"tablespoons",
                          "tablespoon":"tablespoons",
                          "tsp":"teaspoons",
                          "teaspoon":"teaspoons",
                          "kg":"kilograms",
                          "kilogram":"kilograms"}


## determines if the value is of the form
#   <#>"unitString" (one word) or is just a number
#   splits it if it is 
def splitByNum(string):
    regex = re.compile("^\d+\.*\d*|^\d*\.\d+")
    m = regex.match(string)
    if m == None:
        print "false"
        return False, [string, '']
    else:
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
def tryParseNum(string):
    amount = 0
    unitString = ""    
    #print "recieved :", string

    isDone,indexList = splitByNum(string)
    
    tempList = []
    tempList.append(string[indexList[0][0]:indexList[0][1]])
    tempList.append(string[indexList[1][0]:indexList[1][1]])
    #print "got back: ", isDone, "  ", tempList
    #print
    if isDone:
        # of the form <#>"unitString" or just <#>
        amount = float(tempList[0])
        if not tempList[1] == "":
            unitString = abbreviatedUnitStrings[tempList[1]]
        return True,[amount,unitString]
    else:
        # not of that form
        # check if it is a number first
        if tempList[0] in numberWords.keys():
            amount = numberWords[tempList[0]]
            return True,[amount]
        else:
            # there are no numbers, don't know how to parse this thing so we return false
            # hopefully this is because it is of the form "oil for cooking" or somehting like that
            return False, []

## this presumes the list is split already
## will look through to match the following
## returns False if no hyphen is present
## otherwise will return True and modify the string to make it easier to read       
def handleAmount(string):
    # scan the string and find all instances of the form:
    # number - number || number "to" number
    regex = re.compile("\d*\s*-\s*\d*\D?|\d*\s*to\s*\d*\D?")
    m = regex.match(string)

    if m == None:
        print "track"
        found = False
        stringList = string.split()        
        for s in stringList:
            print "all day: ",s
            # examine each word in the ingredient string, see if we can
            # find a number
            foundNum,indexList = splitByNum(s)
            if foundNum:
                found = True
                break
            else:
                # wasn't in digit form, check for word form
                if s.lower() in numberWords.keys():
                    # remove the number word from the string
                    # and return the values
                    print "got to here!"
                    found = True
                    stringList.pop(stringList.index(s))
                    newString = ""
                    for w in stringList:
                        newString += w + " "
                    return True,newString, numberWords[s.lower()],""
                                        
        if not found:
            #no numbers
            return False, string, "", ""
        else:
            unitString = string[indexList[1][0]:indexList[1][1]]
            amount = string[indexList[0][0]:indexList[0][1]]
            return True, cutUpString(string,indexList[0][0],indexList[1][1]), amount, unitString
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

        string = cutUpString(string,m.span()[0],m.span()[1]).rstrip().lstrip()
        #print "here you go!:", string

        isParseAble1,result1 = tryParseNum(n[0])
        #print "first:", isParseAble1, "  ", result1        
        isParseAble2,result2 = tryParseNum(n[1])
        #print "segundo:", isParseAble2, "  ", result2

        if isParseAble1 and isParseAble2:
            #print "result 1:", result1
            #print "result 2:", result2
            avg = (float(result1[0]) + float(result2[0]))/2.0
            return True,string, avg,result2[1]                
        else:
            print "FUCK!!"
            # throw an error here for handling back in the main program

def handleUnitString(string):
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
                    
        for word in preModifiers:
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

def handleNameModifier(stringList):
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

def cutUpString(string, start, end):
    p1 = string[0:start]
    p2 = string[end:len(string)]
    return p1 + p2

def removePointlessWords(string):
    for w in pointlessWords:
        #regex = re.compile("^\s*"+w+"\s")
        print "checking: ", w
        string = _removePointlessWords(string, w)

    return string

def _removePointlessWords(string, regex):
    newString = ""
    for s in string.split():
        #m = regex.match(s)
        if not s.lower() == regex:
            print "     didn't find in: ", s
            newString += s + " "

            #if not m == None:            
            #    name = cutUpString(name,m.span()[0],m.span()[1])
    return newString

def insertWord(string, word, index):
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

def start(string):
    initialString = string
    string = removePointlessWords(string)
    amount = 0
    name = ""
    modifiers = ""

    print "         string is :", string

    cont,string,amount,unitString = handleAmount(string)
    if not cont:
        print "could not parse, name = ", initialString
        ## this needs to actually create an ingredient, set amount = 1
        return initialString        
    if unitString == "":
        #print "got to this point"
        cont,string,unitString,modifiers = handleUnitString(string)
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
        name,modifier = handleNameModifier(string.split())
        
    unitString = unitString.lower()
    name = name.lower()
    modifiers = modifiers.lower()

    if unitString == "":
        unitString = name
    elif unitString == "can":
        name = insertWord(name, "can", 0)
        unitString = name
    else:
        if unitString in abbreviatedUnitStrings.keys():
            unitString = abbreviatedUnitStrings[unitString]
    

    print "thus far:"
    print "     name: ", name
    print "     modifiers: ", modifiers
    print "     amount: ", amount
    print "     unitString: ", unitString

    return "name: "+ name +",   modifiers: " + modifiers + ",   amount: " + str(amount) +"   unitString: " + unitString




thisString = "1 to 10 oodles of noodles"
print "working on: ", thisString
start(thisString)
#thisString = insertWord(thisString, "can", 0)
#print thisString
#print "finished: ", removePointlessWords(thisString)

#string = "5 to 10"
#print "5 to 10"
#print
regex = re.compile("\d*\s*to\s*\d*\D?")
#m = regex.match(string)
#print string[m.span()[0] : m.span()[1]]



# finagle a bagle
# womp

x = """
500g dried beehoon
10 prawns
Half a can of luncheon meat, cubed
Half a head of cabbage, shredded
1 medium-sized squid, sliced
1.5 litres of water
4 garlic cloves, chopped
2 purple onions, sliced
1 egg, beaten
Oil for cooking
Seasoning
2 tbsp fish sauce
2 tbsp oyster sauce
2 tbsp soya sauce
White pepper
5 oodles bootyof
1 to 10 oodles of noodles"""


print
print
print
ingList = x.split("\n")
parsedIngList = []
print ingList
for ing in ingList:
    print
    print
    parsedIngList.append(start(ing))

for ing in parsedIngList:
    print ing







