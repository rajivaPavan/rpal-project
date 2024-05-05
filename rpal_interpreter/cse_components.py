import pprint
from rpal_interpreter.nodes import Nodes
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
        for i in controlStruct.getArray():
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
    
    def __init__(self, index):
        """
        Represents a control structure in the CSE machine.
        eg: delta1, delta 0
        """
        self.__index = index
        self.__array: List[Symbol] = []

    def getIndex(self):
        return self.__index
    
    def getArray(self):
        return self.__array

    def addSymbol(self, symbol: Symbol):
        self.__array.append(symbol)

    def __repr__(self):
        return f"delta-{self.__index} = {self.__array}"
        
class ControlStructures:
        
    def __init__(self, st:STNode):
        """Define the Array of Control Structures as a dictionary."""
        self.__initializeCS(st)
        
        
    def __initializeCS(self,st) -> dict:
        """Generates the control structures for the CSE machine from the Standardized Tree.
        Returns: a dictionary of control structures."""
        
        def traverse(node: STNode, deltaIndex: int):
            """
            Traverse the tree using pre-order traversal.
            
            Args:
            node (STNode): The node to traverse.
            csIndex (int): The index of the control structure.
            """

            if node is None:
                return
            
            visit(node, deltaIndex)
            # if node is lambda dont traverse left instead traverse right of left
            if not node.is_lambda():
                traverse(node.getLeft(), deltaIndex)
            traverse(node.getRight(), deltaIndex)

        def visit(node:STNode, deltaIndex: int):
            """
            Visit the node and add the symbol to the control structure.
            """
            currentCS:ControlStruct = self.get(deltaIndex)
            symbol = None
            if node.is_lambda():
                deltaIndex += 1
                deltaIndex = self.__addNewControlStruct(deltaIndex)

                # add x to the control structure
                x:STNode = node.getLeft()
                x_value = x.parseValueInToken()
                symbol = LambdaSymbol(deltaIndex, [x_value])
                currentCS.addSymbol(symbol)
                traverse(x.getRight(), deltaIndex)
            else:
                # add to current CS 
                symbol = SymbolFactory.createSymbol(node)
                currentCS.addSymbol(symbol)
            return deltaIndex

        # Initialize the control structure map
        self.__controlStructureMap = {}   
        # create the control structure for delta 0
        deltaIndex = 0
        self.__addNewControlStruct(deltaIndex)

        # start the traversal from the root of the tree
        traverse(st, deltaIndex)
        pprint.pp(self.__controlStructureMap)
        return self.__controlStructureMap

    def __addNewControlStruct(self, deltaIndex: int):
        while deltaIndex in self.__controlStructureMap.keys():
            deltaIndex+=1
        self.__controlStructureMap[deltaIndex] = ControlStruct(deltaIndex)
        return deltaIndex

    def get(self, deltaIndex) -> ControlStruct:
        """Returns the control struct for the given key."""	
        return self.__controlStructureMap[deltaIndex]
                



