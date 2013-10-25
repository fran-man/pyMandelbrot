'''
Created on 22 Oct 2013

@author: George
'''

import png
from complex import *
from decimal import *
from pixArray import *

# Setup
#getcontext().prec = 28

# Start with a 300x300 image

imgSource = pixArray(100,100)

png.from_array(imgSource.Array, 'RGB').save('a.png')
# def evaluatePixel(xCoord,yCoord):
#     curr_zn_ = 0 # The variable that will be looped through the formula
#     count = 0 # No. of iterations
#     while curr_zn <=4:
#         
# def iterateMandelbrot(zn):
#     
# def squareComplex(re,im):