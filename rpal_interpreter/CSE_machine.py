from .symbol import *
from .cse_control import *
from .cse_stack import *
from .cse_environment import *
class CSEMachine:
    
    """
    The CSE machine for the RPAL interpreter.
    Evaluates the program when the Standard Tree is given.
    
    """
    
    def __init__(self, st):
        
        #Can only have one control and one stack -> singleton ?
        self.controlStructs = 
        self.control = Control(st)
        self.env = Environment(None, None, 0, None)
        self.stack = Stack()
        
        
    def generateControlStructs(self, st) -> list:
        """Calls the preorder traversal of the ST to generate the control structures."""	
        self.traversePreOrder(st)
        
    def traversePreOrder(self, st):
        """Traverses the ST in preorder to generate the control structures."""
        # not implemented
        if st.root == None:
            return
    

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
            
            top = self.stack.popStack()
            
            if top.isType(Operator):
                __operator = top.operator
                rator = self.stack.popStack()
                
                if self.control.peekRightMost.isType(Gamma):
                    self.control.removeRightMost()
                    rand = self.stack.popStack()
                    self.Stack.calculate(__operator, rator, rand)

                else:
                    self.calculate(__operator, rator)
                    
            if top.isType(LambdaClosure):
                
                self.env = Environment(None, Environment )
            
            
        if right_most.isType(Lambda):
            
            #Have to go back in the control to get the env index of the lambda closure. did not implement yet
            envIndex = 
            self.stack.pushStack(LambdaClosure(right_most.variable, right_most.index, envIndex))
        
        
        if right_most.isType(EnvMarker):
            self.stack.removeElement(right_most)
            
        
        
        
        else:
            self.stack.pushStack(right_most)
            
        self.evaluate()
        
        
        


    
    
        

    


    
    