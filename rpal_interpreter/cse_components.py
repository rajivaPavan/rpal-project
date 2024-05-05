from rpal_interpreter.trees import STNode
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
        right_most = self.control.pop(-1)
        return right_most
        
    def insertControlStruct(self, controlStruct) :
        for i in controlStruct:
            self.control.append(i)
            
    def insertEnvMarker(self, env_index):
        self.control.append(EnvMarkerSymbol(env_index))
            

class Stack:
    
    """
    The stack to evaluate the CONTROL.
    """    
    
    def __init__(self):
        self.stack = [EnvMarkerSymbol(0)]
    
    def popStack(self) -> Symbol:
        popElement = self.stack.pop(0)
        return popElement
    
    def pushStack(self, symbol: Symbol):
        self.stack.append(symbol)
    
    def removeEnvironment(self, envMarker: EnvMarkerSymbol):
        self.stack.remove(envMarker)
        
        
class Environment:
    
    """
    Represents the environments of the CSE machine as a tree structure. 
    Initially the environment is the Primitive Environment.
    
    """
    
    def __init__(self, parent = None, envIndex = None):
        """
        Initialize environments.
        envData is represented as a dictionary.
        """
        self.parent : Environment = parent
        self.envMarker = EnvMarkerSymbol(envIndex)
        self.envData = {}      
        
        
        
    def insertEnvData(self, name, value):
        
        """Inserts the values for the variables in the environment."""  
        self.envData[name] = value
        
    def getEnvData(self,name):
        return self.envData[name]
    
        
    def lookUpEnv(self, name: str):
        
        """
        Looks up the value for the variable.
        Checks the parent environment if not in the current.
        
        """
        
        if name in self.envData:
            return self.envData[name]
        
        else:
            return self.parent.lookUpEnv(name)
        
class ControlStruct:
    
    def __init__(self, index = None):
        
        """
        Represents a control structure in the CSE machine.
        eg: delta1, delta 0
        """
        
        self.index = index
        self.controlStruct: List[Symbol] = []
        
class ControlStructures:
        
        def __init__(self, st:STNode):
            """Define the Array of Control Structures as a dictionary."""
            self.__controlStructureMap = self.__generateControlStructures(st)
            
            
        def __generateControlStructures(self,st) -> dict:
            """Generates the control structures for the CSE machine from the Standardized Tree.
            Returns: a dictionary of control structures."""	
            #TODO: Implement the generation of control structures
            st = st
            pass
            
        def addControlStruct(self, controlStruct: ControlStruct):
            """Adds a control struct to the control structure map with the control struct index as the key."""
            self.__controlStructureMap[controlStruct.index] = controlStruct
            
        def get(self, key) -> ControlStruct:
            """Returns the control struct for the given key."""	
            return self.__controlStructureMap[key]
                    


    
    