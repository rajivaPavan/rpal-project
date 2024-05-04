from .symbol import *

class Control:
    
    """The control of the CSE machine."""
    
    def __init__(self, controlStructs):
        self.control = [EnvMarker(0)].insertControlStructs(controlStructs[0])  
     
    
    def peekRightMost(self):
        right_most = self.control[-1]
        return right_most
    
    def removeRightMost(self):
        right_most = self.control.pop(-1)
        return right_most
        
    def insertControlStructs(self, controlStruct):
        for i in controlStruct.controlStruct:
            self.control.append(i)
            
            
            
