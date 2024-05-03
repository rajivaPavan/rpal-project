class Symbol:
    def __init__(self, type):
        pass
        
    def isType(self, t):
        return self.__class__ == t
    
class Variable(Symbol):
    def __init__(self, name):
        super().__init__()
        self.name = name  
        
class EnvMarker(Symbol):
    def __init__(self, envIndex):
        super().__init__()
        
         
        
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
        self.envIndex = envIndex
        
        
        

## additional
class CommaSymbole(Symbol):
    def __init__(self):
        super().__init__()
        
class Fcn_Form(Symbol):
    def __init__(self):
        super().__init()
        
class Tau(Symbol):
    def __init__(self):
        super().__init()

class Operator(Symbol):
    def __init__(self, operator, value):
        super().__init()
        self.operator = operator
        value = value


        

        
