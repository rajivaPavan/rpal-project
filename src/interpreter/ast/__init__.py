from interpreter.ast.nodes import Nodes
from structs.tree import BinaryTreeNode, TreeFormatter

class ASTNode(BinaryTreeNode):
    """
    A class representing a node in an Abstract Syntax Tree (AST).

    The ASTNode class uses the left child right sibling representation to store the tree structure.
    Each node contains a reference to its node value, left child, and right sibling.
    """
    def __init__(self, value, left=None, right=None):
        super().__init__(value, left, right)

    def __str__(self, level=0):
        """
        Returns a string representation of the current node and its children.
        
        Args:
            level (int): The current level of the node in the tree.
        
        Returns:
            str: A string representation of the current node and its children.
        """
        
        _formatter = TreeFormatter
        value = str(self.getValue())
        if value in Nodes.TYPES:
            value = f"<{value}>"
        s = value
        if self.getLeft() != None:
            child_level = level + 1
            line = _formatter.line_str(self.getLeft(), child_level)
            s += line
        if self.getRight() != None:
            line = _formatter.line_str(self.getRight(), level)
            s += line
        return s