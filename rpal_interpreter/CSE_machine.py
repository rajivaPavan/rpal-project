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

        elif right_most.isType(NameSymbol):
            _nameSymbol = right_most
            self.stackaName(_nameSymbol)       
              
        elif right_most.isType(LambdaSymbol):
            _lambda = right_most
            self.stackLambda(_lambda)
                   
        elif right_most.isType(BinaryOperatorSymbol):
            _binop = right_most.operator
            self.binop(_binop)
            
        elif right_most.isType(UnaryOperatorSymbol):
            _unop = right_most.operator
            self.unop(_unop)
            
        elif right_most.isType(GammaSymbol):
            self.applyLambda()
            
        elif right_most.isType(EnvMarkerSymbol):
            env_marker = right_most
            self.exitEnv(env_marker)
            
        elif right_most.isType():
            self.conditional()
            
        else:
            pass
            #Should throw an exception
               
        self.evaluate()
        
        
          
    def stackaName(self, nameSymbol: NameSymbol):
        
        """
        CSE Rule 1
        
        Pushes the value of the name symbol into the stack.
        
        """
        
        if nameSymbol.checkNameSymbolType(int):
            __value = nameSymbol.name
        
        elif nameSymbol.checkNameSymbolType(str):
            __value = self.env.lookUpEnv(nameSymbol.name)
            
        self.stack.pushStack(__value)
        
            
            
    def stackLambda(self, _lambda: LambdaSymbol):
        
        """
        
        CSE Rule 2
        
        Pushes a lambda closure into the stack.
        
        """
        
        __currentEnvIndex = self.env.envMarker.envIndex
        self.stack.pushStack(LambdaClosureSymbol(_lambda.variables, _lambda.index, __currentEnvIndex))         
            
    def applyLambda(self):
        
        """
        
        CSE Rule 4
        
        creates a new environment.
        
        """	
        
        top = self.stack.popStack() 
        
        if top.isType(LambdaClosureSymbol):
            
            __lambdaClosure: LambdaClosureSymbol = top
            
            __env_index = __lambdaClosure.envMarker.envIndex + 1
            __new_env = Environment(self.env, __env_index, None )
            self.env = __new_env    
            for var in __lambdaClosure.variables:
                self.env.insertEnvData(var, self.stack.popStack())
                
            self.addEnvMarker(__env_index)
            
            self.control.insertControlStruct(self.controlStructArray.getControlStruct(__lambdaClosure.index))
            
    def addEnvMarker(self, env_index):
            
        """
        Adds an environment marker to the stack and the control.
        
        """
        
        self.stack.pushStack(EnvMarkerSymbol(env_index))
        self.control.insertEnvMarker(env_index)
            
    def exitEnv(self, env_marker):
        
        """
        CSE Rule 5
        
        Exits from the current environment.
        
        """
        
        self.stack.removeElement(env_marker)
        self.env = self.env.parent
        
        
    def binop(self, operator):
        
        """
        CSE Rule 6
        
        Evaluates Binary Operators and pushes the computed result into the stack.
        
        """
        rand_1 = self.stack.popStack()
        rand_2 = self.stack.popStack()
        self.stack.pushStack(self.apply(operator, rand_1, rand_2))
        
    def unop(self, operator):
        
        """"
        CSE Rule 7
        
        Evaluates Unary Operators and pushes the computed result into the stack.
        
        """
        rand = self.stack.popStack()
        self.stack.pushStack(self.apply(operator, rand))
            
    def apply(self, operator, rator, rand = None):
        
        """
        
        Applies the operator to the operands.
        
        """
        if self.isOperator(operator, "+"):
            result = rator + rand
        elif self.isOperator(operator, "-"):
            result = rator - rand
        elif self.isOperator(operator, "*"):
            result = rator * rand
        elif self.isOperator(operator, "/"):
            result = rator / rand
        elif self.isOperator(operator, "or"):
            result = rator or rand
        elif self.isOperator(operator, "and"):
            result = rator and rand
        elif self.isOperator(operator, ".gr"):
            result = rator > rand
        elif self.isOperator(operator, "ge"):
            result = rator >= rand
        elif self.isOperator(operator, "ls"):
            result = rator < rand
        elif self.isOperator(operator, "le"):
            result = rator <= rand
        elif self.isOperator(operator, "eq"):
            result = rator == rand
        elif self.isOperator(operator, "neg"):
            result = -rator
        elif self.isOperator(operator, "not"):
            result = not rator
        
            
        return result    
        
        
    def isOperator(operator, type):
        
        """
        
        Takes an operator as an argument and returns whether its of the given type
        
        """
        
        return operator == type
    
    
    
    def conditional(self):
        """
        CSE Rule 8
        
        """
        pass
    
    def tupleFormation(self):
        """
        CSE Rule 9
        
        """
        pass
    
    def tupleSelection(self):
        
        """
        
        CSE Rule 10
        """
        pass
    
    
    
    
        
        
    
    

        
        


    
        

    


    
    