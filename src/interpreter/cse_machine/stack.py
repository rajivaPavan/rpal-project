from typing import List
from .symbol import EnvMarkerSymbol, Symbol


class Stack:
    
    """
    The stack to evaluate the CONTROL.
    """    
    
    def __init__(self):
        self.__arr: List[Symbol] = []

    def popStack(self) -> Symbol:
        popElement = self.__arr.pop(0)
        return popElement
    
    def top(self) -> Symbol:
        return self.__arr[0]
    
    def pushStack(self, symbol: Symbol):
        self.__arr.insert(0,symbol)
    
    def removeEnvironment(self, envMarker: EnvMarkerSymbol):
        self.__arr.remove(envMarker)

    def __repr__(self) -> str:
        return f"{self.__arr}"
 