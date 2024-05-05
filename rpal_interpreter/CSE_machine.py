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
        
        """Evaluates the Control."""
        
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
            
        elif right_most.isType(BetaSymbol):
            self.conditional()
            
        else:
            pass
            #TODO: throw an exception
               
        self.evaluate()
        
        
          
    def stackaName(self, nameSymbol: NameSymbol):
        
        """
        CSE Rule 1
        
        Pushes the value of the name symbol into the stack.
        
        """
        
        if nameSymbol.checkNameSymbolType(int):
            _value = nameSymbol.name
        
        elif nameSymbol.checkNameSymbolType(str):
            _value = self.env.lookUpEnv(nameSymbol.name)
            
        self.stack.pushStack(NameSymbol(_value))
        
            
            
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
            
            _lambdaClosure: LambdaClosureSymbol = top
            
            env_index = _lambdaClosure.envMarker.envIndex + 1
            new_env = Environment(self.env, env_index, None )
            self.env = new_env    
            for var in _lambdaClosure.variables:
                self.env.insertEnvData(var, self.stack.popStack())
                
            self.addEnvMarker(env_index)
            
            self.control.insertControlStruct(self.controlStructArray.getControlStruct(_lambdaClosure.index))
            
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
        
    operator_map = {
        
        "+": lambda rator, rand: rator + rand,
        "-": lambda rator, rand: rator - rand,
        "*": lambda rator, rand: rator * rand,
        "/": lambda rator, rand: rator / rand,
        "or": lambda rator, rand: rator or rand,
        "and": lambda rator, rand: rator and rand,
        "gr": lambda rator, rand: rator > rand,
        "ge": lambda rator, rand: rator >= rand,
        "ls": lambda rator, rand: rator < rand,
        "le": lambda rator, rand: rator <= rand,
        "eq": lambda rator, rand: rator == rand,
        "neg": lambda rator: -rator,
        "not": lambda rator: not rator
        
    }
        
        
    def binop(self, operator):
        
        """
        CSE Rule 6
        
        Evaluates Binary Operators and pushes the computed result into the stack.
        
        """
        rand_1 = self.stack.popStack().name
        rand_2 = self.stack.popStack().name
        _value = self.apply(operator, rand_1, rand_2)
        self.stack.pushStack(NameSymbol(_value))
        
    def unop(self, operator):
        
        """"
        CSE Rule 7
        
        Evaluates Unary Operators and pushes the computed result into the stack.
        
        """
        rand = self.stack.popStack().name
        _value = NameSymbol(self.apply(operator, rand))
        self.stack.pushStack(NameSymbol(_value))
        
    
            
    def apply(self, operator, rator, rand = None):
        
        """
        
        Applies the operator to the operands.
        
        """ 
        if rand is None:
            return self.operator_map[operator](rator)
        else:
            return self.operator_map[operator](rator, rand)
    
    
    
    
    def conditional(self):
        """
        CSE Rule 8
        
        This evaluates the conditional expression.
        Conditional functions are defined in the control in the form of delta_then, delta_else, beta, B.
        
        
        """
        then_or_else = self.stack.popStack()
        if then_or_else.name == True:
            self.control.removeRightMost()
            _then: DeltaSymbol = self.control.removeRightMost()
            self.control.insertControlStruct(_then.index)
        else:
            _else: DeltaSymbol = self.control.removeRightMost()
            self.control.removeRightMost()
            self.control.insertControlStruct(self.controlStructArray.getControlStruct(_else.index))
        
        
    
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
    
    
    
    
        
        
    
    

        
        


    
        

    


    
    