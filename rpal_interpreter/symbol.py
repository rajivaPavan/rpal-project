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
        
class OperatorSymbol(Symbol):
    def __init__(self, operator):
        super().__init()
        self.operator = operator
        
              
class GammaSymbol(Symbol):
    """Represents a gamma Symbol in the CSE machine."""
    
    def __init__(self):
        super().__init__()
        
class LambdaSymbol(Symbol):
    """Represents a lambda Symbol in the CSE machine."""
    
    def __init__(self, variables, index):
        super().__init__()
        self.variables = []
        self.index = index
        
        for var in variables:
            self.variables.append(var)


class LambdaClosureSymbol(LambdaSymbol):
    
    """Represents a lambda closure (lambda in the stack) in the CSE machine.
    
        Has the additional attribute envIndex.
        
        Extends the Lambda class.
    """
    
    
    def __init__(self, variable, index, envIndex):
        super().__init__(variable, index)
        self.envMarker: EnvMarkerSymbol = EnvMarkerSymbol(envIndex)
        

class EnvMarkerSymbol(Symbol):
    
    """ Represents an environment marker in the CSE machine. """
    
    def __init__(self, envIndex):
        super().__init__()
        self.envIndex = envIndex
        
class BetaSymbol(Symbol):
    def __init__(self):
        super().__init__()
        

class TauSymbol(Symbol):
    def __init__(self, n):
        super().__init()
        self.n = n




        

        
