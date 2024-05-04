from .symbol import *

class Stack:
    
    """
    The stack to evaluate the CONTROL.
    """    
    
    def __init__(self):
        self.stack = [EnvMarker(0)]
    
    def popStack(self):
        popElement = self.stack.pop(0)
        return popElement
    
    def pushStack(self, value):
        self.stack.append(value)
        
        
    #Removes the first occurence of the value
    # def removeElement(self, value):
    #     self.remove(value)
        
    # def negFunction(self, rator):
    #     return -rator
    
    # def minusFunction(self, rator, rand):
    #     return rator - rand
    
    # def plusFunction(self, rator, rand):
    #     return rator + rand

    # def expFunction(self, rator, rand):
    #     return pow(rator, rand)
    
    # def multiFunction(self, rator, rand):
    #     return rator * rand   
        
        
    def apply(self, operator, rator, rand = None):
        if operator == "neg":
            result = -rator
        elif operator == "+":
            result = rator + rand
        elif operator == "-":
            result = rator - rand
        elif operator == "*":
            result = rator * rand
        elif operator == "/":
            result = rator / rand
        elif operator == "**":
            result = pow(rator, rand)
                
        self.stack.pushStack(result)
