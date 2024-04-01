from .parser import Parser
from .tokens import *
class RPALParser(Parser):
    def __init__(self,src):
        super().__init__(src)
        
        
    def __Rn(self):
        """TODO: Add Docstring for this method and implement this method correctly."""
        token = self.nextToken()
        if token.__class__ == IdentifierToken:
            pass
        elif token.__class__ == IntegerToken:
            pass
        elif token.__class__ == StringToken:
            pass
        elif token.__class__ == LParenToken:
            pass
        else:
            raise Exception("Invalid token")

    def parse(self):
            """Parses the source program and returns the Abstract Syntax Tree (AST).

            Returns:
                The Abstract Syntax Tree (AST) of the source program.
            """
            return self.getAST()
    
