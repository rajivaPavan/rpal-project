from rpal_interpreter.nodes import Nodes


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
            s += _formatter.line_str(self.getLeft(), child_level)
        if self.getRight() != None:
            s += _formatter.line_str(self.getRight(), level)
        return s

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
    
    @staticmethod
    def assign_node(left = None, right = None):
        """
        Creates a new assign node in the form of a FCRS node.
        """
        return STNode.createFCRSNode(Nodes.ASSIGN, left, right)
        
    

            

    
    
        
    
 