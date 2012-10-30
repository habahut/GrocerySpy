


nums="""
1
one	2
two	3
three	4
four	5
five	6
six	7
seven	8
eight	9
nine	10
ten
11
eleven	12
twelve	13
thirteen	14
fourteen	15
fifteen	16
sixteen	17
seventeen	18
eighteen	19
nineteen	20
twenty
21
twenty-
one	22
twenty-
two	23
twenty-
three	24
twenty-
four	25
twenty-
five	26
twenty-
six	27
twenty-
seven	28
twenty-
eight	29
twenty-
nine	30
thirty
31
thirty-
one	32
thirty-
two	33
thirty-
three	34
thirty-
four	35
thirty-
five	36
thirty-
six	37
thirty-
seven	38
thirty-
eight	39
thirty-
nine	40
forty
41
forty-
one	42
forty-
two	43
forty-
three	44
forty-
four	45
forty-
five	46
forty-
six	47
forty-
seven	48
forty-
eight	49
forty-
nine	50
fifty
51
fifty-
one	52
fifty-
two	53
fifty-
three	54
fifty-
four	55
fifty-
five	56
fifty-
six	57
fifty-
seven	58
fifty-
eight	59
fifty-
nine	60
sixty
61
sixty-
one	62
sixty-
two	63
sixty-
three	64
sixty-
four	65
sixty-
five	66
sixty-
six	67
sixty-
seven	68
sixty-
eight	69
sixty-
nine	70
seventy
71
seventy-
one	72
seventy-
two	73
seventy-
three	74
seventy-
four	75
seventy-
five	76
seventy-
six	77
seventy-
seven	78
seventy-
eight	79
seventy-
nine	80
eighty
81
eighty-
one	82
eighty-
two	83
eighty-
three	84
eighty-
four	85
eighty-
five	86
eighty-
six	87
eighty-
seven	88
eighty-
eight	89
eighty-
nine	90
ninety
91
ninety-
one	92
ninety-
two	93
ninety-
three	94
ninety-
four	95
ninety-
five	96
ninety-
six	97
ninety-
seven	98
ninety-
eight	99
ninety-
nine"""


## reorder it
preNums = []
for letter in nums:
    preNums.append(letter)

for letter in range(len(preNums)-1,0, -1):
    if preNums[letter] == "-":
        preNums.pop(letter+1)

## recompile the string
newString = ""
for letter in range(len(preNums)):
    newString += preNums[letter]

## add in non-hyphenated versions
numsList = newString.split()

for i in range(len(numsList)-1,0,-1):
    if not (numsList[i].find("-") == -1):
        # this is the one we need to strip the hyphen from
        hyphenIndex = numsList[i].find("-")
        strippedHyphen = numsList[i][0:hyphenIndex] + " " + numsList[i][
            hyphenIndex + 1:len(numsList[i])]
        numsList.insert(i+1,strippedHyphen)

        # this is the number
        numsList.insert(i+1,numsList[i-1])

theDict = {}
for i in range(0,len(numsList), 2):
    #print numsList[i], numsList[i+1]
    theDict[numsList[i+1]] = float(numsList[i])

theDict["half"] = float(.5)
theDict["eighth"] = float(.125)
theDict["quarter"] = float(.25)

#print theDict

anotherDict = {'sixty-one': 61.0, 'seventy-two': 72.0, 'thirty one': 31.0, 'fifty-one': 51.0, 'seventy nine': 79.0, 'sixty-two': 62.0, 'fifty': 50.0, 'four': 4.0, 'forty-six': 46.0, 'twenty-three': 23.0, 'ninety six': 96.0, 'eighty one': 81.0, 'seventy-seven': 77.0, 'fifty six': 56.0, 'sixty two': 62.0, 'twenty two': 22.0, 'eighty-four': 84.0, 'forty eight': 48.0, 'fifty four': 54.0, 'ninety eight': 98.0, 'seventy five': 75.0, 'ninety five': 95.0, 'seventy-five': 75.0, 'forty-nine': 49.0, 'seventy three': 73.0, 'five': 5.0, 'twenty five': 25.0, 'half': 0.5, 'sixteen': 16.0, 'forty-five': 45.0, 'sixty-nine': 69.0, 'eighty six': 86.0, 'fifty seven': 57.0, 'twenty nine': 29.0, 'sixty four': 64.0, 'forty-four': 44.0, 'fifty-six': 56.0, 'twenty six': 26.0, 'ninety-two': 92.0, 'thirty-eight': 38.0, 'quarter': 0.25, 'forty one': 41.0, 'sixty-five': 65.0, 'twelve': 12.0, 'seventeen': 17.0, 'fifty three': 53.0, 'ten': 10.0, 'ninety one': 91.0, 'sixty three': 63.0, 'thirty seven': 37.0, 'ninety nine': 99.0, 'thirteen': 13.0, 'thirty six': 36.0, 'thirty two': 32.0, 'seventy-four': 74.0, 'ninety-one': 91.0, 'forty': 40.0, 'forty five': 45.0, 'forty-three': 43.0, 'seventy six': 76.0, 'twenty-five': 25.0, 'eighty four': 84.0, 'sixty-eight': 68.0, 'seventy-eight': 78.0, 'eighty three': 83.0, 'forty four': 44.0, 'ninety-nine': 99.0, 'forty-seven': 47.0, 'ninety-three': 93.0, 'sixty nine': 69.0, 'fourteen': 14.0, 'forty seven': 47.0, 'fifty-seven': 57.0, 'sixty': 60.0, 'fifteen': 15.0, 'seventy': 70.0, 'fifty one': 51.0, 'sixty seven': 67.0, 'thirty': 30.0, 'twenty-seven': 27.0, 'seventy-three': 73.0, 'fifty-four': 54.0, 'eighty eight': 88.0, 'forty six': 46.0, 'thirty nine': 39.0, 'sixty-three': 63.0, 'twenty-six': 26.0, 'twenty-two': 22.0, 'seventy-six': 76.0, 'ninety two': 92.0, 'sixty-six': 66.0, 'thirty-one': 31.0, 'one': 1.0, 'eighty-seven': 87.0, 'ninety': 90.0, 'forty two': 42.0, 'fifty nine': 59.0, 'seventy-one': 71.0, 'ninety seven': 97.0, 'thirty five': 35.0, 'fifty-three': 53.0, 'seventy-nine': 79.0, 'twenty': 20.0, 'sixty-seven': 67.0, 'two': 2.0, 'eighth': 0.125, 'seventy seven': 77.0, 'eleven': 11.0, 'ninety four': 94.0, 'eighty-two': 82.0, 'twenty seven': 27.0, 'twenty-eight': 28.0, 'seventy one': 71.0, 'eighty-one': 81.0, 'seventy eight': 78.0, 'ninety-seven': 97.0, 'nineteen': 19.0, 'eighty nine': 89.0, 'eighty-three': 83.0, 'twenty-one': 21.0, 'forty three': 43.0, 'fifty five': 55.0, 'twenty one': 21.0, 'sixty six': 66.0, 'fifty two': 52.0, 'nine': 9.0, 'three': 3.0, 'thirty-five': 35.0, 'sixty one': 61.0, 'twenty-four': 24.0, 'ninety-six': 96.0, 'fifty-nine': 59.0, 'seven': 7.0, 'seventy two': 72.0, 'thirty-nine': 39.0, 'sixty-four': 64.0, 'sixty eight': 68.0, 'forty nine': 49.0, 'eighteen': 18.0, 'fifty-eight': 58.0, 'ninety-five': 95.0, 'thirty-three': 33.0, 'thirty four': 34.0, 'eighty seven': 87.0, 'ninety three': 93.0, 'six': 6.0, 'fifty-five': 55.0, 'eighty two': 82.0, 'fifty eight': 58.0, 'forty-one': 41.0, 'eighty-six': 86.0, 'eight': 8.0, 'ninety-eight': 98.0, 'twenty four': 24.0, 'eighty': 80.0, 'thirty-six': 36.0, 'thirty-two': 32.0, 'eighty-eight': 88.0, 'thirty-seven': 37.0, 'eighty-nine': 89.0, 'ninety-four': 94.0, 'thirty three': 33.0, 'twenty eight': 28.0, 'twenty-nine': 29.0, 'thirty eight': 38.0, 'eighty five': 85.0, 'seventy four': 74.0, 'forty-two': 42.0, 'forty-eight': 48.0, 'thirty-four': 34.0, 'sixty five': 65.0, 'eighty-five': 85.0, 'fifty-two': 52.0, 'twenty three': 23.0}
print anotherDict


    
