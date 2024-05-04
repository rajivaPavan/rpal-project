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

class TreeFormatter():

    @staticmethod
    def line_str(node, level):
        return "\n" + "." * level + node.__str__(level)
        
class ASTNode(BinaryTreeNode):
    """A class representing a node in an Abstract Syntax Tree (AST).

    The ASTNode class uses the left child right sibling representation to store the tree structure.
    Each node contains a reference to its node value, left child, and right sibling.
    """
    
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
    
class STNode(BinaryTreeNode):
        
    def __str__(self, level = 0):
        """
        Returns a string representation of the tree using pre-order traversal.
        """
        
        _formatter = TreeFormatter
        
        s = str(self.getValue())
        _left = self.getLeft()
        _right = self.getRight()
        
        if _left is not None:
            s += _formatter.line_str(_left, level)
        if _right is not None:
            s += _formatter.line_str(_right, level)
        return s
    

            

    
    
        
    
 