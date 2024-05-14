from interpreter.cse_machine.exceptions import MachineException
from interpreter.cse_machine.functions import FunctionFactory
from .symbol import *
from typing import List

                
class Environment:
    """
    Represents the environments of the CSE machine as a tree structure. 
    
    Attributes:
        envMarker (EnvMarkerSymbol): The environment marker symbol.
        parent (Environment): The parent environment.
        envData (dict): The data in the environment.
        
    Methods:
        insertEnvData(name: str, value: Symbol): Inserts the values for the variables in the environment.
        lookUpEnv(name: str) -> Symbol: Looks up the relevant value for a given variable.
    """
    
    def __init__(self, envIndex, parent = None):
        
        self.envMarker = EnvMarkerSymbol(envIndex)
        self.parent : Environment = parent
        self.envData = {}    
        
    def getIndex(self):
        return self.envMarker.envIndex
        
        
    def insertEnvData(self, name, value):
        self.envData[name] = value
    
        
    def lookUpEnv(self, name: str):

        # check if the name is a defined function in the primitive environment
        if self.parent is None:
            if DefinedFunctions.isdefined(name):
                # add a function symbol with the defined Function Object
                return FunctionSymbol(FunctionFactory.create(name))
            else:
                raise MachineException(f"{name} is not defined")
            
        if name in self.envData:
            return self.envData[name]
        else:
            return self.parent.lookUpEnv(name)
        
    def __repr__(self) -> str:
        p = "None"
        if self.parent is not None:
            p = self.parent.envMarker
        return f"{self.envMarker}: {self.envData}, p - {p}"
            

        
