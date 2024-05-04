from .symbol import *
class CSEMachine:
    
    """
    The CSE machine for the RPAL interpreter.
    Evaluates the program when the Standard Tree is given.
    
    """
    
    def __init__(self, st):
        self.control = Control(st)
        self.env = Environment(None, None, 0, None)
        self.stack = Stack()
    

    def evaluate(self):
        
        """Evaluates the CSE machine."""
        
        right_most = self.control.removeRightMost()
        
        if right_most.isType(None):
            return self.stack.popStack()
        
        if right_most.isType(Primitive):  
            self.stack.pushStack(right_most.value)
            

        if right_most.isType(Name):
            """
            Looks up the value for the variable in the environment.
            pushes the respective value to the stack.
            """
            __value = self.env.lookUpEnv(right_most.name)
            self.stack.pushStack(__value)
            
        
        if right_most.isType(Operator):
            self.stack.pushStack(right_most)
        
        if right_most.isType(Gamma):
            #only implemented the evaluation of an operator, has to be changed
            operator = self.stack.popStack().operator
            rator = self.stack.popStack()
            
            if self.control.peekRightMost.isType(Gamma):
                self.control.removeRightMost()
                rand = self.stack.popStack()
                self.Stack.calculate(operator, rator, rand)

            else:
                self.calculate(operator, rator)
            
           

        if right_most.isType(EnvMarker):
            self.stack.removeElement(right_most)
            
        
        if right_most.isType(Lambda):
            pass
        
        else:
            self.stack.pushStack(right_most)
            
        self.evaluate()
        

class Control:
    
    """The control of the CSE machine."""
    
    def __init__(self, st):
        
        self.controlStructs: ControlStruct = self.generateControlStructs(st)    #an array which contains the control structures
        self.control = [EnvMarker(0)].insertControlStructs(self.controlStructs[0])  #
        
        
    def generateControlStructs(self, st) -> list:
        """Calls the preorder traversal of the ST to generate the control structures."""	
        self.traversePreOrder(st)
        
    def traversePreOrder(self, st):
        """Traverses the ST in preorder to generate the control structures."""
        # not implemented
        if st.root == None:
            return

    
    def peekRightMost(self):
        right_most = self.control[-1]
        return right_most
    
    def removeRightMost(self):
        right_most = self.control.pop(-1)
        return right_most
        
    def insertControlStructs(self, controlStruct):
        for i in controlStruct.controlStruct:
            self.control.append(i)
            
            
            
class ControlStruct:
    
    def __init__(self, index):
        
        """
        Represents a control structure in the CSE machine.
        eg: delta1, delta 0
        """
        
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
        
    def lookUpEnv(self, name):
        
        """
        Looks up the value for the variable.
        Checks the parent environment if not in the current.
        
        """
        
        if name in self.envData:
            return self.envData[name]
        
        else:
            return self.parent.lookUpEnv(name)
        

    
    