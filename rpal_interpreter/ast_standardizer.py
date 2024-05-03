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