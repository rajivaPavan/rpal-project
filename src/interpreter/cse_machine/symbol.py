from typing import Iterable
from interpreter.ast.nodes import Nodes
from interpreter.cse_machine.functions import DefinedFunctions
from .st import STNode
from logger import logger

class Symbol:
    
    """
    Represents differnt types of symbols in the CSE machine.
    Include both control symbols and stack symbols.
    
    """
    
    def __init__(self):
        pass
        
    def isType(self, t):
        return self.__class__ == t

    def __eq__(self, other):
        return id(self) == id(other)
    
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
            # elif value in DefinedFunctions.PREDFINED:
            #     return FunctionSymbol(node.getN(), [])

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
    Represents variables and numerics in the CSE machine.
    """
    def __repr__(self):
        return f"{self.name}"
    
    def __init__(self, name):
        super().__init__()
        self.name = name  
        self.nameType = name.__class__
        
    def checkNameSymbolType(self, dataType):
        if not(self.isPrimitive() or self.isTupleSymbol()):
            raise Exception(f"Invalid type for NameSymbol:{dataType}")
        return self.nameType == dataType
    
    def isPrimitive(self):
        return self.nameType == str or self.nameType == int or self.nameType == bool
    
    def isTupleSymbol(self):
        return self.nameType == TupleSymbol
    
            
class OperatorSymbol(Symbol):
    def __init__(self, operator):
        super().__init__()
        self.operator = operator
        
    def __repr__(self):
        return f"{self.operator}"
    
class FunctionSymbol(Symbol):

    def __init__(self, func):
        super().__init__()
        self.func = func

    def __repr__(self):
        return f"<{self.func}>"
    
    
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
    
    def __repr__(self):
        return f"<lambda, ({', '.join(self.variables)}), {self.index}, {self.envMarker}>"
    

class EtaClosureSymbol(LambdaClosureSymbol):
        """Represents an eta closure in the CSE machine.
        
        Extends the LambdaClosure class.
        """
        
        def __init__(self, variables, index, envIndex):
            super().__init__(variables, index, envIndex)
        
        def __repr__(self):
            return f"<eta, ({', '.join(self.variables)}), {self.index}, {self.envMarker}>"
        
        @staticmethod
        def fromLambdaClosure(lambdaClosure:LambdaClosureSymbol):
            """Creates an eta closure from a lambda closure."""
            return EtaClosureSymbol(lambdaClosure.variables, lambdaClosure.index, lambdaClosure.getEnvMarkerIndex())
        
        @staticmethod
        def toLambdaClosure(etaClosure):
            """Converts an eta closure to a lambda closure."""
            return LambdaClosureSymbol(etaClosure.variables, etaClosure.index, etaClosure.getEnvMarkerIndex())

class EnvMarkerSymbol(Symbol):
    
    """ Represents an environment marker in the control and the stack. """
    
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
    Has an index which points to relevant control structure in the control structure array.

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
        return f"({', '.join([str(tup_el) for tup_el in self.tuple])})"


class YStarSymbol(Symbol):
    
    """
    Represents a Y* symbol in the CSE machine.
    """

    def __repr__(self):
        return f"Y*"


        

        
