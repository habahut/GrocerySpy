#! /usr/bin/env python

import sys
#print sys.version


from main import Main


GrocerySpy = Main()

GrocerySpy.run()

"""
include number word analysis in ingredient parser

also, if ingredient is neither number or number word, then maybe just store
it as a modifier, with 0 as amount and name?

also, compiling a list of values, maybe with a text interface
might be easier for building the name, amount, unitString premodifiers database
"""
