from .symbol import *
from typing import List

class Control:
    
    """The control of the CSE machine."""
    
    def __init__(self, controlStruct):
        self.control: List[Symbol] = []
        self.insertEnvMarker(0)
        self.insertControlStruct(controlStruct)  
    
    def peekRightMost(self):
        #Not used yet.
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
    
    def popStack(self):
        popElement = self.stack.pop(0)
        return popElement
    
    def pushStack(self, value):
        self.stack.append(value)
    
    def removeElement(self, envMarker):
        self.stack.remove(envMarker)
        
        
class Environment:
    
    """
    Represents the environments of the CSE machine as a tree structure. 
    Initially the environment is the Primitive Environment.
    
    """
    
    def __init__(self, parent = None, envIndex = None, envData = None):
        """
        Initialize environments.
        envData is represented as a dictionary.
        """
        self.parent : Environment = parent
        self.envMarker = EnvMarkerSymbol(envIndex)
        self.envData = {}      
        
        
        
    def insertEnvData(self, name, value):
        
        """Inserts the value for the variable in the environment."""  
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
        
class ControlStructArray:
        
        def __init__(self, st):
            """Define the Array of Control Structures as a dictionary."""
            self.controlStructArray = {}
            self.controlStructArray = self.generateControlStructArray(st)
            
            
        def generateControlStructArray(self,st):
            #TODO: Implement the generation of control structures
            st = st
            pass
            
        def addControlStruct(self, controlStruct: ControlStruct):
            self.controlStructArray[controlStruct.index] = controlStruct
            
        def getControlStruct(self, index):
            return self.controlStructArray[index]
        
        def getControlStructArray(self):
            return self.controlStructArray
                    


    
    