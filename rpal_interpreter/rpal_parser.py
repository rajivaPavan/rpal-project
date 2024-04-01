from .parser import Parser
from .tokens import *
class RPALParser(Parser):
    def __init__(self,src):
        super().__init__(src)
        
        
    def __Rn(self):
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
        """returns the AST of the src program"""
        return self.getAST()
    
