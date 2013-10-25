'''
Created on 25 Oct 2013

@author: George
'''

class pixArray(object):
    '''
    classdocs
    '''


    def __init__(self,xSize,ySize):
        self.Array = [[0 for x in range(xSize*3)] for x in range(ySize)]
    
    def getRaw(self):
        return self.Array
    
    def setPixel(self,xVal,yVal,red,green,blue):
        self.Array[yVal][3*xVal] = red
        self.Array[yVal][3*xVal + 1] = green
        self.Array[yVal][3*xVal + 2] = blue