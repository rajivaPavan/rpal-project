from structs.tree import BinaryTreeNode

class ASTNode(BinaryTreeNode):
    """A class representing a node in an Abstract Syntax Tree (AST).

    The ASTNode class uses the left child right sibling representation to store the tree structure.
    Each node contains a reference to its node value, left child, and right sibling.
    """
    def __init__(self, value, left=None, right=None):
        super().__init__(value, left, right)