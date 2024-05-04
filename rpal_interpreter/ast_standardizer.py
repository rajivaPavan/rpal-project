from rpal_interpreter.nodes import Nodes
from rpal_interpreter.trees import STNode, ASTNode


class ASTStandardizer:
    """
    A class that standardizes an Abstract Syntax Tree (AST).
    """

    def __init__(self):
        self.st:STNode = None  # Standardized Tree

    def standardize(self, ast:ASTNode)->STNode:
        """
        Standardizes the given AST.

        Args:
            ast: The input Abstract Syntax Tree (AST) to be standardized.

        Returns:
            Root of the standardized tree.
        """
        
        return self.st
        
    # list of values of nodes that do not need to be standardized
    NON_STANDARDIZE = Nodes.UOP + Nodes.BOP + [
        Nodes.TAU, 
        Nodes.ARROW, 
        Nodes.COMMA
    ]

    def __standardize(self, node:ASTNode)->STNode:
        val = node.getValue()
        if val in ASTStandardizer.NON_STANDARDIZE:
            # no need to standardize the node, make a copy of it
            return STNode.copy(node)

