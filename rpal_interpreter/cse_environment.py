from .symbol import *

class Environment:
    
    """
    Represents the environments of the CSE machine as a tree structure. 
    Initially the environment is the Primitive Environment.
    
    """
    
    def __init__(self, child=None, parent = None, envMarker = None, envData = None):
        """
        Initialize environments.
        envData is represented as a dictionary.
        """
        envMarker: EnvMarker = envMarker
        self.children = []
        self.parent : Environment = parent
        self.envData = {}      
        
        if child is not None:
            self.children.append(child)
        
    def insertEnvData(self, name, value):
        
        """Inserts the value for the variable in the environment."""  
        self.envData[name] = value
        
    def getEnvData(self,name):
        return self.envData[name]
    
        
    def lookUpEnv(self, name):
        
        """
        Looks up the value for the variable.
        Checks the parent environment if not in the current.
        
        """
        
        if name in self.envData:
            return self.envData[name]
        
        else:
            return self.parent.lookUpEnv(name)
        