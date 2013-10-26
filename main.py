'''
Created on 22 Oct 2013

@author: George
'''

import png
from complex import *
from decimal import *
from pixArray import *

# Setup Defaults
#getcontext().prec = 28
# Mandelbrot World Parameters
xMin = -2
xMax = 1
yMin = -0.845
yMax = 0.845
xRange = abs(xMin) + abs(xMax)
yRange = abs(yMin) + abs(yMax)

imgWidth = 300
scaleFactor = imgWidth/xRange 

# Start with a 300x300 image

imgSource = pixArray(100,100)

for i in range(0,100):
    imgSource.setPixel(i, i, 2*i, 0, 0)
    #print str(i)

png.from_array(imgSource.getRaw(), 'RGB').save('a.png')

def pixToIm(pixel_X,pixel_Y):
    '''
    Convert a pixel's xy coordinate into
    a complex number with decimal coefficients
    '''
    img_X = pixel_X/scaleFactor + xMin # Div by scaleFactor maps to range [0,xRange].
    img_Y = pixel_Y/scaleFactor + yMin
    return Complex(img_X,img_Y)
# def evaluatePixel(xCoord,yCoord):
#     curr_zn_ = 0 # The variable that will be looped through the formula
#     count = 0 # No. of iterations
#     while curr_zn <=4:
#         
# def iterateMandelbrot(zn):
#     
# def squareComplex(re,im):