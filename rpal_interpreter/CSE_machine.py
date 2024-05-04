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

        self.controlStructs = self.generateControlStructs(st)
        self.control = Control(self.controlStructs)
        self.env = Environment(None, 0, None)
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
            __operator = right_most.operator
            rand_1 = self.stack.popStack()
            __unop = {'neg', 'not'}                 #Have to define these correctly
            
            if __operator in __unop:
                self.apply(__operator, rand_1)
            else:
                rand_2 = self.stack.popStack()
                self.apply(__operator, rand_1, rand_2)
                
                
        if right_most.isType(Lambda):
            envIndex = self.env.envMarker.envIndex
            self.stack.pushStack(LambdaClosure(right_most.variable, right_most.index, envIndex))   

        
        if right_most.isType(Gamma):
            
            __top = self.stack.popStack() 
            if __top.isType(LambdaClosure):
                __env_index = __top.envMarker.envIndex + 1
                __new_env = Environment(self.env, __env_index, None )
                self.env = __new_env    
                self.env.insertEnvData(__top.variable, self.stack.popStack())
                
        
        if right_most.isType(EnvMarker):
            self.stack.removeElement(right_most)
            
        
        
        
        else:
            self.stack.pushStack(right_most)
            
        self.evaluate()
        
        
        
    def generateControlStructs(self, st) -> list:
        """Calls the preorder traversal of the ST to generate the control structures."""	
        self.traversePreOrder(st)
        
    
        
        
        


    
    
        

    


    
    