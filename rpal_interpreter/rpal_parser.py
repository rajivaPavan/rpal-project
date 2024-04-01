from .parser import Parser
from .tokens import *
class RPALParser(Parser):
    def __init__(self,src):
        super().__init__(src)
        
        
    def __Rn(self):
        """Parse the Rn production rule.

        Raises:
            Exception: If an invalid token is encountered.

        Returns:
            None
        """
        token = self.nextToken()
        if token.__class__ == IdentifierToken:
            self.read(token)
            if token.value in ["true", "false", "nil", "dummy"]:
                self.buildTree(token.value, 0)
            pass
        elif token.__class__ in [IntegerToken, StringToken]:
            self.read(token)
        elif token.__class__ == LParenToken:
            self.read(token, ignore=True)
        else:
            raise Exception("Invalid token")

    def parse(self):
            """Parses the source program and returns the Abstract Syntax Tree (AST).

            Returns:
                The Abstract Syntax Tree (AST) of the source program.
            """
            return self.getAST()
    
