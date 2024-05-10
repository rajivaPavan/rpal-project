from typing import Iterable
from interpreter.ast.nodes import Nodes
from interpreter.cse_machine.functions import DefinedFunctions
from .st import STNode
from logger import logger

class Symbol:
    
    """Represents symbols in the CSE machine."""
    
    def __init__(self):
        pass
        
    def isType(self, t):
        return self.__class__ == t

    def __eq__(self, other):
        return id(self) == id(other)
    
class SymbolFactory:
    
    """A factory class to create symbols from the ST nodes."""
    
    @staticmethod
    def createSymbol(node:STNode):
        value = node.getValue()
        if node.is_gamma():
            return GammaSymbol()
        elif node.is_name():
            node: STNode = node
            is_id = node.is_id()
            value = node.parseValueInToken()
            if str.isnumeric(value):
                value = int(value)
            return NameSymbol(value, is_id)
        elif value in [Nodes.TRUE, Nodes.FALSE]:
            value = value == Nodes.TRUE
            return NameSymbol(value)
        elif value in [Nodes.DUMMY, Nodes.NIL]:
            return NameSymbol(value)
        elif value in Nodes.BOP:
            return BinaryOperatorSymbol(value)
        elif value in Nodes.UOP:
            return UnaryOperatorSymbol(value)
        elif value is Nodes.YSTAR:
            return YStarSymbol()
        else:
            logger.error(f"Invalid node type:{value}")
            raise Exception(f"Invalid node type:{value}")

#Subclasses of Symbol
class NameSymbol(Symbol):
    """
    Represents variables and numerics as a symbol.
    
    Methods:
        isId() -> bool: Returns the ID.
        isFunction() -> bool: Returns True if the symbol is a function.
        isString() -> bool: Returns True if the symbol is a string.
        isPrimitive(nameType) -> bool: Returns True if the symbol is a string integer or a bool.
        isTupleSymbol(nameType) -> bool: Returns True if the symbol is a TupleSymbol.
        isValidType(nameType) -> bool: Returns True if the symbol is a valid type.
    
    """
    def __repr__(self):
        return f"{self.name}"
    
    def __init__(self, name, is_id = False):
        super().__init__()
        self.name = name  
        self.nameType = name.__class__
        self.is_id = is_id

    def isId(self):
        return self.is_id

    def isFunction(self):
        return self.name in DefinedFunctions.get_functions()

    def isString(self):
        return self.nameType == str
    
    @staticmethod
    def isPrimitive(nameType):
        return nameType == str or nameType == int or nameType == bool
    
    @staticmethod
    def isTupleSymbol(nameType):
        return nameType == TupleSymbol
    
    @staticmethod
    def isValidType(nameType):
        return NameSymbol.isPrimitive(nameType) or NameSymbol.isTupleSymbol(nameType)
            
class OperatorSymbol(Symbol):
    """"Represents an operator symbol."""
    def __init__(self, operator):
        super().__init__()
        self.operator = operator
        
    def __repr__(self):
        return f"{self.operator}"
    
class FunctionSymbol(Symbol):
    """Represents a function symbol."""

    def __init__(self, func):
        super().__init__()
        self.func = func

    def __repr__(self):
        return f"<{self.func}>"
    
    
class BinaryOperatorSymbol(OperatorSymbol):
    """Represents a binary operator symbol."""
    def __init__(self, operator):
        super().__init__(operator)

        
class UnaryOperatorSymbol(OperatorSymbol):
    """Represents a unary operator symbol."""
    def __init__(self, operator):
        super().__init__(operator)
        
              
class GammaSymbol(Symbol):
    """Represents a gamma Symbol."""
    
    def __init__(self):
        super().__init__()
        
    def __repr__(self):
        return f"gamma"
    
class LambdaSymbol(Symbol):
    """
    Represents a lambda Symbol,.
    
    Attributes:
        index (int): The index of the lambda in the control structure array.
        variables (Iterable): The variables of the lambda.
    """
    
    def __init__(self, index, variables:Iterable):
        super().__init__()
        self.index = index
        self.variables = tuple(variables)

    def __repr__(self):
        return f"<lambda, ({', '.join(self.variables)}), {self.index}>"
        
class LambdaClosureSymbol(LambdaSymbol):
    """
    Represents a lambda closure (lambda in the stack) in the CSE machine.
    
    Extends the Lambda class.
    
    
    Attributes:
        envMarker (EnvMarkerSymbol): The environment marker the lambda closure.    
    """
    
    def __init__(self, variables, index, envIndex):
        super().__init__(index, variables)
        self.envMarker: EnvMarkerSymbol = EnvMarkerSymbol(envIndex)
    
    def getEnvMarkerIndex(self):
        return self.envMarker.envIndex
    
    def __repr__(self):
        return f"<lambda, ({', '.join(self.variables)}), {self.index}, {self.envMarker}>"
    

class EtaClosureSymbol(LambdaClosureSymbol):
    """
    Represents an eta closure in the CSE machine.
    
    Extends the LambdaClosure class.
    
    Methods: 
        fromLambdaClosure(lambdaClosure:LambdaClosureSymbol) -> EtaClosureSymbol: Creates an eta closure from a lambda closure.
        toLambdaClosure(etaClosure) -> LambdaClosureSymbol: Converts an eta closure to a lambda closure.
    """
    
    def __init__(self, variables, index, envIndex):
        super().__init__(variables, index, envIndex)
    
    def __repr__(self):
        return f"<eta, ({', '.join(self.variables)}), {self.index}, {self.envMarker}>"
    
    @staticmethod
    def fromLambdaClosure(lambdaClosure:LambdaClosureSymbol):
        
        return EtaClosureSymbol(lambdaClosure.variables, lambdaClosure.index, lambdaClosure.getEnvMarkerIndex())
    
    @staticmethod
    def toLambdaClosure(etaClosure):
        
        return LambdaClosureSymbol(etaClosure.variables, etaClosure.index, etaClosure.getEnvMarkerIndex())

class EnvMarkerSymbol(Symbol):
    
    """
    Represents an environment marker in the control and the stack. 
    
    Attributes:
        envIndex (int): The index of the environment marker.
        
    Methods:
        __eq__(other) -> bool: Checks whether an instance of the EnvMarkerSymbol and then checks whether equal.
    """
    
    def __init__(self, envIndex):
        super().__init__()
        self.envIndex = envIndex

    def __repr__(self) -> str:
        return f"e{self.envIndex}"
    
    def __eq__(self, other):
        if not isinstance(other, EnvMarkerSymbol):
            return False
        return self.envIndex == other.envIndex
        
class DeltaSymbol(Symbol):
    
    """
    Represents a control structure as a Symbol in the control.
    
    Attributes: 
        index (int): Points to relevant control structure in the control structure array.

    """
    
    def __init__(self, index):
        super().__init__()
        self.index = index

    def __repr__(self) -> str:
        return f"delta-{self.index}"

class BetaSymbol(Symbol):
    
    """ 
    Represents a beta symbol.
    
    Used when representing a conditonal operator in the control without standardizing.
    
    """
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f"beta"
        

class TauSymbol(Symbol):
    
    """
    Represents a tau symbol.
    
    Used when representing a tau node in the control.	
    """
    def __init__(self, n):
        super().__init__()
        self.n = n

    def __repr__(self):
        return f"<tau:{self.n}>"
        
class TupleSymbol(TauSymbol):
    """
    Represents a Tuple in the stack as an object.
    
    Used in standardizing the tau node in the st.
    """
    def __init__(self, n, tupleList):
        super().__init__(n)
        self.tuple = tuple(tupleList)

    def __repr__(self):
        tuple_ = ','.join([str(tup_el) for tup_el in self.tuple])
        tuple_ = tuple_.strip(',')
        return f"({tuple_})"


class YStarSymbol(Symbol):
    
    """Represents a Y* symbol."""

    def __repr__(self):
        return f"Y*"


        

        
