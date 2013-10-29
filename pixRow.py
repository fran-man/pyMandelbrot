'''
Created on 25 Oct 2013

@author: George
'''

class pixRow(object):
    '''
    classdocs
    '''


    def __init__(self,xSize):
        self.Array = [0 for x in range(xSize*3)]
    
    def getRaw(self):
        return self.Array
    
    def setPixel(self,xVal,red,green,blue):
        self.Array[3*xVal] = red
        self.Array[3*xVal + 1] = green
        self.Array[3*xVal + 2] = blue