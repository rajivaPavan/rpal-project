from .symbol import *
from .cse_components import *
class CSEMachine:
    
    """
    Evaluates the program when the Standard Tree is given.
    
    """
    
    def __init__(self, st):

        self.controlStructArray = ControlStructArray(st)
        self.control = Control(self.controlStructArray)
        self.env = Environment(None, 0, None)
        self.stack = Stack()
        

    def evaluate(self):
        
        """Evaluates the CSE machine."""
        
        right_most = self.control.removeRightMost()
        
        if right_most.isType(None):
            final_result = self.stack.popStack()
            return final_result

        if right_most.isType(Name):
            __name = right_most.name
            self.stackaName(__name)
              
              
        if right_most.isType(Lambda):
            __lambda = right_most
            self.stackLambda(__lambda)
               
               
        if right_most.isType(Operator):
            __operator = right_most.operator
            self.evaluateOperator(__operator)
            
        if right_most.isType(Gamma):
            self.applyLambda()
            
        if right_most.isType(EnvMarker):
            __env_marker = right_most
            self.exitEnv(__env_marker)
            
        if right_most.isType(FcnForm):
            self.conditional()
               
        self.evaluate()
        
        
          
    def stackaName(self, name):
        
        """
        Rule 1
        Pushes the value of the symbol onto the stack.
        
        """
        
        if name.isnumeric():
            __value = name
            self.stack.pushStack(int(__value))
        
        else:
            __value = self.env.lookUpEnv(name)
            self.stack.pushStack(__value)
            
            
            
    def stackLambda(self, _lambda):
        
        """
        
        Rule 2
        Pushes a lambda closure onto the stack.
        
        """
        
        envIndex = self.env.envMarker.envIndex
        self.stack.pushStack(LambdaClosure(_lambda.variable, _lambda.index, envIndex)) 
        
    def evaluateOperator(self, operator):
        
        """
        Rule number 6 and 7 
        as the minimally sufficient conditions for the rule 3
        
        Evaluates binary and unary operators.
        Calls the apply method to apply the operator accordingly.
        
        """
        
        
        rand_1 = self.stack.popStack()
        __unop = {'neg', 'not'}                 #Have to define these correctly
        
        if operator in __unop:
            self.apply(operator, rand_1)
        else:
            rand_2 = self.stack.popStack()
            self.apply(operator, rand_1, rand_2)
            
            
    def apply(self, operator, rator, rand = None):
        
        """
        
        Applies the operator to the operands.
        
        """
        
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
            
            
    def applyLambda(self):
        
        """
        
        Rule 4
        
        creates a new environment.
        
        """	
        
        __top = self.stack.popStack() 
        if __top.isType(LambdaClosure):
            __env_index = __top.envMarker.envIndex + 1
            __new_env = Environment(self.env, __env_index, None )
            self.env = __new_env    
            self.env.insertEnvData(__top.variable, self.stack.popStack())
            
            self.control.insertControlStructs(self.controlStructArray[__top.index])
            
    def exitEnv(self, env_marker):
        
        """
        Rule 5
        
        Exits from the current environment.
        
        """
        
        self.stack.removeElement(env_marker)
        self.env = self.env.parent
        
    def conditional(self):
        """
        Rule 8
        
        """
        pass
    
    def tupleFormation(self):
        """
        Rule 9
        
        """
        pass
    
    def tupleSelection(self):
        
        """
        
        Rule 10
        """
        pass
    
    def n_aryEunction(self):
        
        """
        Rule 11
        
        """
        pass
    
    
        
        
    
    

        
        


    
        

    


    
    