from .symbol import *

class Control:
    
    """The control of the CSE machine."""
    
    def __init__(self, st):
        
        self.controlStructs: ControlStruct = self.generateControlStructs(st)    #an array which contains the control structures
        self.control = [EnvMarker(0)].insertControlStructs(self.controlStructs[0])  #
        
        
    def generateControlStructs(self, st) -> list:
        """Calls the preorder traversal of the ST to generate the control structures."""	
        self.traversePreOrder(st)
        
    def traversePreOrder(self, st):
        """Traverses the ST in preorder to generate the control structures."""
        # not implemented
        if st.root == None:
            return

    
    def peekRightMost(self):
        right_most = self.control[-1]
        return right_most
    
    def removeRightMost(self):
        right_most = self.control.pop(-1)
        return right_most
        
    def insertControlStructs(self, controlStruct):
        for i in controlStruct.controlStruct:
            self.control.append(i)
            
            
            
class ControlStruct:
    
    def __init__(self, index):
        
        """
        Represents a control structure in the CSE machine.
        eg: delta1, delta 0
        """
        
        self.index = index
        self.controlStruct = []