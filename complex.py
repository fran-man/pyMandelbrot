'''
Created on 24 Oct 2013

@author: George
'''

from decimal import *

class Complex:
    '''
    classdocs
    '''
    

    def __init__(self, rePart,imPart):
                self.Re = rePart
                self.Im = imPart
    
    def square(self):
        result_Real = self.Re**2 + (self.Im**2)*(-1)
        result_Imaginary = 2*self.Re*self.Im
        finalResult = Complex(result_Real,result_Imaginary)
        return finalResult
    
    def modulus(self):
        return (self.Re**2 + self.Im**2)**Decimal(0.5)