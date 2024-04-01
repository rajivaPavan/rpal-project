class ASTNode:
    """A class representing a node in an Abstract Syntax Tree (AST).

    The ASTNode class uses the left child right sibling representation to store the tree structure.
    Each node contains a reference to its node value, left child, and right sibling.

    Attributes:
        node: The value of the node.
        left_child: The left child of the node.
        right_sibling: The right sibling of the node.
    """

    def __init__(self, node, left_child=None, right_sibling=None):
        self.node = node
        self.left_child = left_child
        self.right_sibling = right_sibling

    def setLeftChild(self, node):
        self.left_child = node

    def setRightSibling(self, node):
        self.right_sibling = node

    def __str__(self, level=0):
            """
            Returns a string representation of the current node and its children.
            
            Args:
                level (int): The current level of the node in the tree.
            
            Returns:
                str: A string representation of the current node and its children.
            """
            s = str(self.node)
            if self.left_child != None:
                child_level = level + 1
                s += "\n" + "." * child_level + self.left_child.__str__(child_level)
            if self.right_sibling != None:
                s += "\n" + "." * level + self.right_sibling.__str__(level)
            return s
 