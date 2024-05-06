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
        if len(self.control)== 0:
            return None
        right_most = self.control.pop(-1)
        return right_most
        
    def insertControlStruct(self, controlStruct) :
        for i in controlStruct.getArray():
            self.control.append(i)
            
    def insertEnvMarker(self, env_index):
        self.control.append(EnvMarkerSymbol(env_index))

    def __repr__(self):
        return f"{self.control}"
            

class Stack:
    
    """
    The stack to evaluate the CONTROL.
    """    
    
    def __init__(self):
        self.__arr: List[Symbol] = []

    def popStack(self) -> Symbol:
        popElement = self.__arr.pop(0)
        return popElement
    
    def pushStack(self, symbol: Symbol):
        self.__arr.insert(0,symbol)
    
    def removeEnvironment(self, envMarker: EnvMarkerSymbol):
        for i in range(len(self.__arr)):
            if isinstance(self.__arr[i], EnvMarkerSymbol) and self.__arr[i].envIndex == envMarker.envIndex:
                self.__arr.pop(i)
                break

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
            traverse(node.getLeft(), deltaIndex)
            traverse(node.getRight(), deltaIndex)

        def visit(node:STNode, deltaIndex: int):
            """
            Visit the node and add the symbol to the control structure.
            """
            currentCS:ControlStruct = self.get(deltaIndex)
            symbol = None
            if node.is_lambda():
                deltaIndex = self.__addNewControlStruct(deltaIndex)
                # add x to the control structure
                x:STNode = node.getLeft()
                x_value = x.parseValueInToken()
                symbol = LambdaSymbol(deltaIndex, [x_value])
                currentCS.addSymbol(symbol)
                # don't traverse left of lambda
                node.setLeft(None)
                traverse(x.getRight(), deltaIndex)
            elif node.is_conditional():
                # add beta to the control structure
                _handleConditional(node, deltaIndex, currentCS)
            else:
                # add to current CS 
                symbol = SymbolFactory.createSymbol(node)
                currentCS.addSymbol(symbol)
            return deltaIndex

        def _handleConditional(node:STNode, deltaIndex:int, currentCS:ControlStruct):
            symbol = BetaSymbol()
            delta_then = self.__addNewControlStruct(deltaIndex)
            delta_else = self.__addNewControlStruct(delta_then)
            delta_then_symbol = DeltaSymbol(delta_then)
            delta_else_symbol = DeltaSymbol(delta_else)
            currentCS.addSymbol(delta_then_symbol)
            currentCS.addSymbol(delta_else_symbol)
            currentCS.addSymbol(symbol)
            boolean_exp:STNode = node.getLeft()
            # dont traverse left of node
            node.setLeft(None)
            then_exp:STNode = boolean_exp.getRight()
            boolean_exp.setRight(None)
            else_exp:STNode = then_exp.getRight() 
            then_exp.setRight(None)
            traverse(boolean_exp, deltaIndex)
            traverse(then_exp, delta_then)
            traverse(else_exp, delta_else)

        # Initialize the control structure map
        self.__controlStructureMap = {}   
        # create the control structure for delta 0
        deltaIndex = 0
        self.__addNewControlStruct(deltaIndex)

        # start the traversal from the root of the tree
        traverse(st, deltaIndex)
        return self.__controlStructureMap

    def __addNewControlStruct(self, deltaIndex: int):
        """Adds a new control structure to the Control Structure Map by linear probing"""
        while deltaIndex in self.__controlStructureMap.keys():
            deltaIndex+=1
        self.__controlStructureMap[deltaIndex] = ControlStruct(deltaIndex)
        return deltaIndex

    def get(self, deltaIndex) -> ControlStruct:
        """Returns the control struct for the given key."""	
        return self.__controlStructureMap[deltaIndex]
                
    def __repr__(self):
        return pprint.pformat(self.__controlStructureMap)



