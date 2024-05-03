from .symbol import *
class CSEMachine:
    ## How are we going to define the primitive enviromnment?
        
    def __init__(self, st):
        self.control = Control(st)
        self.env = Environment(None, None, 0)
        self.stack = Stack()
    

    def evaluate(self):
        #Only imlemented for binary and unary operators
        #Only half way done
        right_most = self.control.removeRightMost()
        
        if right_most.isType(None):
            return self.stack.popStack()
        
        
        if right_most.isType(Gamma):
            
            operator = self.stack.popStack()
            rator = self.stack.popStack()
            
            if self.control.lookAheadisType.isType(Gamma):
                self.control.removeRightMost()
                rand = self.stack.popStack()
                self.Stack.calculate(operator, rator, rand)

            else:
                self.calculate(operator, rator)
            
           

        if right_most.isType(EnvMarker):
            self.stack.removeElement(right_most)
            pass    
        
        if right_most.isType(Lambda):
            pass
        
        else:
            self.stack.pushStack(right_most)
        
        

class Control:
    
    """Represents a control in the CSE machine."""
    
    def __init__(self, st):
        self.controlStructs = st.preorderTraverse()
        self.control = [EnvMarker(0)].insertControlStructs(self.controlStructs[0])
        
    def preOrderTraverse(self):
        pass
    
    def removeRightMost(self):
        right_most = self.control.pop(-1)
        return right_most
        
    def insertControlStructs(self, controlStruct):
        for i in controlStruct.controlStruct:
            self.control.append(i)
            
    #LookAhead into the control structure
    def lookAhead(self):
        self.control[-1]
            
            
class ControlStruct:
    """
    Represents a control structure in the CSE machine.
    eg: delta1, delta 0
    """
    
    def __init__(self, index):
        self.index = index
        self.controlStruct = []
    
    
        
class Stack:
    
    """
    The stack to evaluate the CONTROL.
    """    
    
    def __init__(self):
        self.__stack = [EnvMarker(0)]
    
    def popStack(self):
        popElement = self.stack.pop(0)
        return popElement
    
    def pushStack(self, value):
        self.stack.append(value)
        
        
    #Removes the first occurence of the value
    def removeElement(self, value):
        self.remove(value)
        
        
        
    def calculate(self, operator, rator, rand = None):
        
        if operator == "neg":
                self.stack.pushStack(-rator)
                
        if operator == "+":
                self.stack.pushStack(rator + rand)

        if operator == "-":
                self.stack.pushStack(rator - rand)
        
        if operator == "*":
                self.stack.pushStack(rator * rand)
                
        if operator == "/":
                self.stack.pushStack(rator / rand)    
    
    
class Environment:
    
    """
    Represents the environment in the CSE machine as a tree node. 
    Initially the environment is the Primitive Environment.
    
    """
    
    def __init__(self, child=None, parent = None, envMarker = None, envData = None):

        ##Initially envData should be PE
        envMarker: EnvMarker = envMarker
        self.children = []
        self.parent : Environment = parent
        self.envData = []
        
    
        

    
    