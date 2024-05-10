from typing import List
from .symbol import EnvMarkerSymbol, Symbol


class Stack:
    
    """
    The stack to evaluate the CONTROL.
    
    Methods:
        popStack() -> Symbol: Pops the top element from the stack.
        top() -> Symbol: Returns the top element of the stack.
        pushStack(symbol: Symbol): Pushes the symbol to the stack.
        removeEnvironment(envMarker: EnvMarkerSymbol): Removes the environment marker from the stack.
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
 