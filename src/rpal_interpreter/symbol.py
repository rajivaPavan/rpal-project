from typing import Iterable
from rpal_interpreter.nodes import Nodes

from rpal_interpreter.trees import STNode


class Symbol:
    
    """
    Represents differnt types of symbols in the CSE machine.
    Include both control symbols and stack symbols.
    
    """
    
    def __init__(self):
        pass
        
    def isType(self, t):
        return self.__class__ == t
    
class SymbolFactory:

    @staticmethod
    def createSymbol(node:STNode):
        value = node.getValue()
        if node.is_gamma():
            return GammaSymbol()
        elif node.is_name():
            value = node.parseValueInToken()
            if str.isnumeric(value):
                value = int(value)
            elif value in [Nodes.TRUE, Nodes.FALSE]:
                value = value == Nodes.TRUE
            elif value in [Nodes.DUMMY, Nodes.NIL]:
                raise NotImplementedError()

            return NameSymbol(value)
        elif value in Nodes.BOP:
            return BinaryOperatorSymbol(value)
        elif value in Nodes.UOP:
            return UnaryOperatorSymbol(value)
        elif value is Nodes.TAU:
            return TauSymbol(value)
        else:
            raise Exception(f"Invalid node type:{value}")

#Subclasses of Symbol
class NameSymbol(Symbol):
    """
    Represents variables and numerics in the CSE machine.
    """
    def __repr__(self):
        return f"{self.name}"
    
    def __init__(self, name):
        super().__init__()
        self.name = name  
        self.type = name.__class__
        
    def checkNameSymbolType(self, dataType):
        assert dataType == str or dataType == int or dataType == bool
        return self.type == dataType
        
class OperatorSymbol(Symbol):
    def __init__(self, operator):
        super().__init__()
        self.operator = operator
        
    def __repr__(self):
        return f"{self.operator}"
    
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
        
    def __repr__(self):
        return f"gamma"
    
class LambdaSymbol(Symbol):
    """Represents a lambda Symbol in the CSE machine.
    
       attribute variables can either be a list or a single variable.
    """
    
    def __init__(self, index, variables:Iterable):
        super().__init__()
        self.index = index
        self.variables = tuple(variables)

    def __repr__(self):
        return f"<lambda, ({', '.join(self.variables)}), {self.index}>"
        
class LambdaClosureSymbol(LambdaSymbol):
    
    """Represents a lambda closure (lambda in the stack) in the CSE machine.
    
        Has the additional attribute envIndex.
        
        Extends the Lambda class.
    """
    
    
    def __init__(self, variables, index, envIndex):
        super().__init__(index, variables)
        self.envMarker: EnvMarkerSymbol = EnvMarkerSymbol(envIndex)
    
    def getEnvMarkerIndex(self):
        return self.envMarker.envIndex
        

class EnvMarkerSymbol(Symbol):
    
    """ Represents an environment marker in the control and the stack. """
    
    def __init__(self, envIndex):
        super().__init__()
        self.envIndex = envIndex

    def __repr__(self) -> str:
        return f"e{self.envIndex}"
        
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
        super().__init__()
        self.n = n

    def __repr__(self):
        return f"tau:{self.n}"
        
class TupleSymbol(TauSymbol):
    """
        Represents a Tuple in the stack as an object.
        Used in standardizing the tau node in the st.
    """
    def __init__(self, n, tupleList):
        super().__init__(n)
        self.tuple = tuple(tupleList)



        

        
