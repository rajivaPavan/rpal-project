from interpreter.cse_machine.functions import FunctionFactory
from .symbol import *
from typing import List

                
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
        
    def getIndex(self):
        return self.envMarker.envIndex
        
        
    def insertEnvData(self, name, value):
        """Inserts the values for the variables in the environment."""  
        self.envData[name] = value
    
        
    def lookUpEnv(self, name: str):
        """
        Looks up the value for the variable.
        Checks the parent environment if not in the current.
        """
        if DefinedFunctions.isdefined(name):
            # add a function symbol with the defined Function Object
            return FunctionSymbol(FunctionFactory.create(name))
               
        if name in self.envData:
            return self.envData[name]
        else:
            return self.parent.lookUpEnv(name)
        
    def __repr__(self) -> str:
        p = "None"
        if self.parent is not None:
            p = self.parent.envMarker
        return f"{self.envMarker}: {self.envData}, p - {p}"
            

        
