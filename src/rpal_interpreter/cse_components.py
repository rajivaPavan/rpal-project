from .symbol import *
from typing import List

class Control:
    
    """The control of the CSE machine."""
    
    def __init__(self, controlStruct):
        self.control: List[Symbol] = []
        self.insertEnvMarker(0)
        self.insertControlStruct(controlStruct)  
    
    def peekRightMost(self):
        #Not used yet. Can remove if needed
        right_most = self.control[-1]
        return right_most
    
    def removeRightMost(self):
        if len(self.control)== 0:
            return None
        right_most = self.control.pop(-1)
        return right_most
        
    def insertControlStruct(self, controlStruct) :
        for i in controlStruct:
            self.control.append(i)
            
    def insertEnvMarker(self, env_index):
        self.control.append(EnvMarkerSymbol(env_index))

    def __repr__(self):
        return f"{self.control}"
    
    def addGamma(self):
        self.control.append(GammaSymbol())
            

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
        
        
class Environment:
    """
    Represents the environments of the CSE machine as a tree structure. 
    Initially the environment is the Primitive Environment.
    """
    
    def __init__(self, envIndex, parent = None):
        """
        Initialize environments.
        envData is represented as a dictionary.
        """
        self.envMarker = EnvMarkerSymbol(envIndex)
        self.parent : Environment = parent
        self.envData = {}      
        
    def insertEnvData(self, name, value):
        """Inserts the values for the variables in the environment."""  
        self.envData[name] = value
    
        
    def lookUpEnv(self, name: str):
        """
        Looks up the value for the variable.
        Checks the parent environment if not in the current.
        """
        
        if name in self.envData:
            return self.envData[name]
        else:
            return self.parent.lookUpEnv(name)
        
    def __repr__(self) -> str:
        p = "None"
        if self.parent is not None:
            p = self.parent.envMarker
        return f"{self.envMarker}: {self.envData}, p - {p}"
            

        
