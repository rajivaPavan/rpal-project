class Symbol:
    
    """
    Represents differnt types of symbols in the CSE machine.
    Include both control symbols and stack symbols.
    
    """
    
    def __init__(self):
        pass
        
    def isType(self, t):
        return self.__class__ == t

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
        assert dataType == str or dataType == int
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
    
    def __init__(self, variables, index):
        super().__init__()
        self.variables = variables
        self.index = index
        
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
    Used when representing a tau node in the control after standardizing.	
    """
    def __init__(self, n):
        super().__init()
        self.n = n




        

        
