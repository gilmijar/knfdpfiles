"""
A formatter/printer for certain KNF DP files: 
When provided with input data it should be able to 
* validate formal correctness
* identify missing entires
* raise exceptions on missing required entries
* print data to target format
* print data to a user-friendly format to help with debugging
Be pythonic, let's try to follow CUPID by DTN
"""

from json import dump
from csv import DictWriter

