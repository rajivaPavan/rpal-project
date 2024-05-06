from rpal_interpreter.nodes import Nodes
from rpal_interpreter.tokens import Token

class BinaryTreeNode:
    """ A class representing a node in a binary tree.
    
    Attributes:
        value: The value of the node.
        left: The left child of the node.
        right: The right child of the node.
    """
    def __init__(self, value, left=None, right=None):
        self.__value = value
        self.__left = left
        self.__right = right
        
    def valueIs(self, value):
        if not isinstance(self.__value, type(value)):
            return False
        return value == self.__value
    
    # getters and setters
    def getValue(self):
        return self.__value
    
    def setValue(self, value):
        self.__value = value
        
    def getLeft(self):
        return self.__left
    
    def setLeft(self, left):
        self.__left = left
        
    def getRight(self):
        return self.__right
    
    def setRight(self, right):
        self.__right = right
    
    @classmethod
    def copy(cls, node):
        """
        Creates a new copy of the given node.
        """
        return cls(node.getValue(), node.getLeft(), node.getRight())
    
    @classmethod
    def deep_copy(cls, node):
        """
        Creates a new deep copy of the given node.
        """
        if node is None:
            return None
        return cls(node.getValue(), STNode.deep_copy(node.getLeft()), STNode.deep_copy(node.getRight()))

    def __str__(self, level=0):
        """
        Returns a string representation of the current node and its children.
        
        Args:
            level (int): The current level of the node in the tree.
        
        Returns:
            str: A string representation of the current node and its children.
        """
        
        _formatter = TreeFormatter
        s = str(self.getValue())
        if self.getLeft() != None:
            child_level = level + 1
            line = _formatter.line_str(self.getLeft(), child_level)
            s += line
        if self.getRight() != None:
            line = _formatter.line_str(self.getRight(), level)
            s += line
        return s
    
    def is_name(self):
        node_value = str(self.getValue())
        return str.startswith(node_value, "<ID:") or str.startswith(node_value, "<INT:") or str.startswith(node_value, "<STR:")
    
    def __repr__(self):
        return f"{self.getValue()}"

class TreeFormatter():

    @staticmethod
    def line_str(node, level):
        return "\n" + "." * level + node.__str__(level)
    
    
        
class ASTNode(BinaryTreeNode):
    """A class representing a node in an Abstract Syntax Tree (AST).

    The ASTNode class uses the left child right sibling representation to store the tree structure.
    Each node contains a reference to its node value, left child, and right sibling.
    """
    def __init__(self, value, left=None, right=None):
        super().__init__(value, left, right)

    
class STNode(BinaryTreeNode):
    """A class representing a node in a Standardized Tree (ST).
    
    The STNode class uses the left child right sibling representation to store the tree structure.
    Each node contains a reference to its node value, left child, and right sibling.
    """

    @staticmethod
    def createFCRSNode(value, left:BinaryTreeNode= None, right:BinaryTreeNode = None):
        """
        Create node with left as first child and right as sibling of first child
        """
        left.setRight(right) 
        node = STNode(value, left, None)
        return node
    
    @staticmethod
    def gamma_node(left = None, right = None):
        """
        Creates a new gamma node in the form of a FCRS node.
        """
        return STNode.createFCRSNode(Nodes.GAMMA, left, right)
    
    @staticmethod
    def lambda_node(left = None, right = None):
        """
        Creates a new lambda node in the form of a FCRS node.
        """
        return STNode.createFCRSNode(Nodes.LAMBDA, left, right)
    
    def is_lambda(self):
        value = self.getValue()
        if not isinstance(value, str):
            return False
        return value == Nodes.LAMBDA
    
    def is_gamma(self):
        value = self.getValue()
        if not isinstance(value, str):
            return False
        return value == Nodes.GAMMA
    
    @staticmethod
    def assign_node(left = None, right = None):
        """
        Creates a new assign node in the form of a FCRS node.
        """
        return STNode.createFCRSNode(Nodes.ASSIGN, left, right)
        
    @staticmethod
    def ystar_node():
        """
        Creates a new ystar node in the form of a FCRS node.
        """
        return STNode(Nodes.YSTAR)
    
    def parseValueInToken(self):
        assert isinstance(self.getValue(), Token)

        token: Token = self.getValue()
        return token.getValue()
    
    

            

    
    
        
    
 