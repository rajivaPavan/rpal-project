from typing import List
from .symbol import EnvMarkerSymbol, GammaSymbol, Symbol


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

    def addSymbol(self, symbol):
        self.control.append(symbol)
 