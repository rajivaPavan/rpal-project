class Symbol:
    
    """
    Represents differnt types of symbols in the CSE machine.
    Include both control symbols and stack symbols.
    
    """
    
    def __init__(self):
        """Implemented in the subclasses."""
        pass
        
    def isType(self, t):
        return self.__class__ == t
        
class Name(Symbol):
    """
    Represents variables and numerics in the CSE machine.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name  
        
class Operator(Symbol):
    def __init__(self, operator):
        super().__init()
        self.operator = operator
        
        
         
        
class Gamma(Symbol):
    """Represents a gamma Node in the CSE machine."""
    
    def __init__(self):
        super().__init__()
        
class Lambda(Symbol):
    """Represents a lambda Node in the CSE machine."""
    
    def __init__(self, variable, index):
        super().__init__()
        self.variable = variable
        self.index = index


class LambdaClosure(Lambda):
    
    """Represents a lambda closure (lambda in the stack) in the CSE machine.
    
        Has the additional attribute envIndex.
        
        Extends the Lambda class.
    """
    
    
    def __init__(self, variable, index, envIndex):
        super().__init__(variable, index)
        self.envMarker: EnvMarker = EnvMarker(envIndex)
        

class EnvMarker(Symbol):
    
    """ Represents an environment marker in the CSE machine. """
    
    def __init__(self, envIndex):
        super().__init__()
        self.envIndex = envIndex
        
class Fcn_Form(Symbol):
    def __init__(self):
        super().__init()
        

## additional
class CommaSymbol(Symbol):
    def __init__(self):
        super().__init__()
        

class Tau(Symbol):
    def __init__(self):
        super().__init()




        

        
