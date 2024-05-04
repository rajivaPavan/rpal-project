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
    def removeElement(self, value):
        self.remove(value)
        
    def negFunction(self, rator):
        return -rator
        
        
        
    def calculate(self, operator, rator, rand = None):
        match operator:
            case "neg":
                self.stack.pushStack(-rator)
            case "+":
                self.stack.pushStack(rator + rand)
            case "-":
                self.stack.pushStack(rator - rand)
            case "*":
                self.stack.pushStack(rator * rand)
            case "/":
                self.stack.pushStack(rator / rand)
            case "**":
                self.stack.pushStack(rator ** rand)
    