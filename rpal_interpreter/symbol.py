from typing import Iterable


class Symbol:
    
    """
    Represents differnt types of symbols in the CSE machine.
    Include both control symbols and stack symbols.
    
    """
    
    def __init__(self):
        pass
        
    def isType(self, t):
        return self.__class__ == t
    
    def __repr__(self):
        # print class name and all attributes and their values
        return f"{self.__class__.__name__}({', '.join(f'{k}={getattr(self, k)}' for k in self.__dict__.keys())})"

#Subclasses of Symbol
class NameSymbol(Symbol):
    """
    Represents variables and numerics in the CSE machine.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name  
        self.type = name.__class__
        
    def checkNameSymbolType(self, dataType):
        assert dataType == str or dataType == int or dataType == bool
        return self.type == dataType
        
class OperatorSymbol(Symbol):
    def __init__(self, operator):
        super().__init()
        self.operator = operator
        
class BinaryOperatorSymbol(OperatorSymbol):
    def __init__(self, operator):
        super().__init__(operator)
        
class UnaryOperatorSymbol(OperatorSymbol):
    def __init__(self, operator):
        super().__init__(operator)
        
              
class GammaSymbol(Symbol):
    """Represents a gamma Symbol in the CSE machine."""
    
    def __init__(self):
        super().__init__()
        
class LambdaSymbol(Symbol):
    """Represents a lambda Symbol in the CSE machine.
    
       attribute variables can either be a list or a single variable.
    """
    
    def __init__(self, index, variables:Iterable):
        super().__init__()
        self.index = index
        self.variables = tuple(variables)
        
class LambdaClosureSymbol(LambdaSymbol):
    
    """Represents a lambda closure (lambda in the stack) in the CSE machine.
    
        Has the additional attribute envIndex.
        
        Extends the Lambda class.
    """
    
    
    def __init__(self, variables, index, envIndex):
        super().__init__(variables, index)
        self.envMarker: EnvMarkerSymbol = EnvMarkerSymbol(envIndex)
        

class EnvMarkerSymbol(Symbol):
    
    """ Represents an environment marker in the control and the stack. """
    
    def __init__(self, envIndex):
        super().__init__()
        self.envIndex = envIndex
        
class DeltaSymbol(Symbol):
    
    """
    Represents a control structure as a Symbol in the control.
    Has an index which points to relevant control structure in the control structure array.
    
    """
    
    def __init__(self, index):
        super().__init()
        self.index = index
        
class BetaSymbol(Symbol):
    
    """ 
    Represents a beta symbol.
    Used when representing a conditonal operator in the control without standardizing.
    
    """
    def __init__(self):
        super().__init__()
        

class TauSymbol(Symbol):
    
    """
    Represents a tau symbol.
    Used when representing a tau node in the control.	
    """
    def __init__(self, n):
        super().__init()
        self.n = n
        
class TupleSymbol(TauSymbol):
    """
        Represents a Tuple in the stack as an object.
        Used in standardizing the tau node in the st.
    """
    def __init__(self, n, tupleList):
        super().__init()
        self.tuple = tuple(tupleList)



        

        
