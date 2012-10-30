#! /usr/bin/env/ python

import pygame
from pygame.locals import *
from pygame import sprite

from utils import loadImage
from pygame.sprite import Sprite
from pygame.sprite import Group

class TextBlock(Sprite):
    ## this is causing problems with wrapping the strings inserting \n
    ## we need to delete \n nearby? but then we will cause things to not align
    # properly, just wrong in a different way....
    def __init__(self, name, stringData, font, locY, maxWidth = 120, maxHeight = 100000):
        pygame.sprite.Sprite.__init__(self)
        self.location = locY
        self.theFont = font

        self.name = name

        self.addText(stringData, maxWidth, maxHeight)

    def addLineBreaks(self, stringData, maxWidth):
        ## first we split it into each individual word
        #stringData = stringData.replace("\n"," ")
        if stringData == None:
            return ""
        
        stringList = stringData.split(" ")

        ## count the letters in each word and add that word to the new string
        # if that word goes over the max length then we need to add \n
        newString = ""
        count = 0
        for word in stringList:
            ## need if else here to control spaces, so there isn't a space at
            # the beginning of each line
            #print 
            if ((count + len(word)) > maxWidth):
                newString += "\n" + word
                count = len(word)
            else:
                newString += word + " "
                count += len(word)

        return newString            
    

    def addText(self, stringData, maxWidth, maxHeight):
        stringData = self.addLineBreaks(stringData, maxWidth)
        allLines = stringData.split("\n")
        
        allTextImages = []
        totalHeight = 0
        widestWidth = 0

        if isinstance(allLines, str):
            #print allLines, " was a string"
            listWrapper = allLines
            allLines = []
            allLines.add(listWrapper)                                       
        
        for line in allLines:            
            thisLineImage = self.theFont.render(line, False, (255,255,255))            
            totalHeight += thisLineImage.get_height()
            if (totalHeight > maxHeight):
                totalHeight -= thisLineImage.get_height()
                #print "     size overflow"
                break
            allTextImages.append(thisLineImage)
            if thisLineImage.get_width() > widestWidth:
                widestWidth = thisLineImage.get_width()
                
        totalHeight += 7
        widestWidth += 50
        self.image = pygame.Surface((widestWidth, totalHeight))
        textBlockCursor = 5
        
        for imageLine in allTextImages:
            self.image.blit(imageLine, (5, textBlockCursor ))
            textBlockCursor += imageLine.get_height()

        self.image.convert()
        
        self.rect = self.image.get_rect()
        x,y = self.rect.topleft
        y += self.location
        self.rect.topleft = x,y

    def get_height(self):
        return self.image.get_height()

    def getName(self):
        return self.name

    def getLeftBorder(self):
        return 55

    def getImage(self):
        return self.image

    def getRect(self):
        return self.rect

    def getBlitPos(self):
        x,y = self.rect.topleft
        x += self.getLeftBorder()
        return x,y

    def updateY(self, dy):
        self.rect.top += dy        

    def collideButtons(self, xy):
        ## even if they did click on the text box, we don't want to do
        # anything to it so we just return None
        return None

    def __str__(self):
        return "textBlock: "+ self.name+ "  @ "+ self.rect.__str__()


if __name__ == "__main__":
    maxWidth = 40

    print maxWidth
    
    """s = ""
    for j in range(10):
        for i in range(50):
            s += str(j) + """

    s = "I have made this recipe hundreds of times...usually use self-rising flour, but I NEVER add any sugar, as I hate sweet tastes, and it always comes out wonderful, but has a definite beer taste. I have added various herbs at times, and have also added various cheeses. Cheddar (mild) is my fav. You also do not have to 'pour butter' on top, or even add it to the mix. I don't add any oil, but I DO dot the top of the bread with pieces of butter. I do not sift the flour and it comes out fine, but I just spoon the flour into a measuring cup. The trick is, do NOT mix a lot, just lightly mix until you have pretty much coated all the flour in the bowl, but no more! Overmixing will give you a hard loaf. If you see a little bit of flour in the bowl, or when you put it in the pan, it is fine...do NOT overmix! I just 'turn it' into a buttered loaf pan, and then I take the spoon and gently 'push' the dough around to make sure it is evenly distributed, especially in the corners...do NOT make it completely level, or push down on it to spread evenly; just light pushing is all you need. It will look lumpy on top...that's better. Then just dot with butter, as much or as little as you want. I also cook it at 350, not 375...you can even use 325 if your oven seems to bake on the hot side. I usually cook it for an hour, but as soon as it is lightly browned on top, I take it out. Sometimes, that is after 55 min., sometimes 1 hour...don't cook longer than an hour, unless you have it on 325 and it is not browned at all. If it is lightly browned and when you push on the top with your finger it seems firm, take it out...1 hour should be sufficient. I let it sit in the pan for just a minute, then I turn it out, and let the loaf lay on it's side on some paper towels. You MUST let it cool, at least 20 minutes, or when you cut it, it will be a gummy mess! It should be cool enough to where you can comfortably hold the loaf with your hand while cutting...if it is too hot to hold, then it is not cool enough. I wait until it is slightly warm, and then cut it...when it is completely cooled, it is fine as well. As I mentioned, it does taste more like 'beer' if you add no sugar, but you do not need it, or any sweetner at all...it will still come out just fine...children would probably like it with some sweetner. Good luck and enjoy! I make it every weekend, as it is quick, and I always have the ingredients on hand....Also, DON'T USE EXPIRED Self-Rising flour, or EXPIRED baking powder!!! I also use ROOM TEMPERATURE BEER, NOT REFRIGERATED! Open the beer, and then pour it into the flour right away, and just stir until coated, NO MORE...DO NOT OVERWORK, VERY IMPORTANT!!!!! Sifting the flour would probably help as well, but I don't...just remember, if you don't sift it, DO NOT PACK IT INTO THE MEASURING CUP! Just spoon it in lightly. Don't be afraid to experiment with different ingredients! Have fun with it!"
    s = s.replace("\n"," ")





"""
    print
    ## need to add a limit to how large a "line" can be
    # must break it up into multiple lines if it is too huge

    ## this asshole. So if there is only one element in the list then
    # it never enters this loop
    newLines = []
    for i in range(0, len(allLines)):
        print "THIS IS THE LENGTH IS OF: "
        print allLines[i]
        length = len(allLines[i])
        print i, " : ", length
        if (length > maxWidth):
            print "got here"
            thisLine = allLines.pop(i)
            while (length > maxWidth):
                newLines.append(thisLine[0:maxWidth])
                thisLine = thisLine[maxWidth + 1:len(thisLine)]
            ## get the remainder
            if not (len(thisLine) == 0):
                newLines.append(thisLine)
        else:
            newLines.append(allLines[i])
    

    for i in newLines:
        print i

"""


