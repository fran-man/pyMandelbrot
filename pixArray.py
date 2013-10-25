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