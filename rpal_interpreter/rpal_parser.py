from .parser import Parser
from .tokens import *
class RPALParser(Parser):
    def __init__(self,src):
        super().__init__(src)
        
    def proc_R(self):
        """Parse the R production rule."""
        
        self.proc_Rn()
        if self.nextToken().__class__ == SemiColonToken:
            # read the semicolon token and ignore it
            self.read(SemiColonToken.instance(), ignore=True)
            
        # check if the next token is a @ 
        token = self.nextToken()
        while token != None and token.isValue("@"):
            # read the @ token and ignore it
            self.read(OperatorToken.fromValue("@"), ignore=True)
            
            # next token should be an identifier
            token = self.nextToken()
            self.read(IdentifierToken.fromValue(token.value))
            
            self.proc_R()
            self.buildTree("@", 3)
        
    def proc_Rn(self):
        """Parse the Rn production rule.

        Raises:
            Exception: If an invalid token is encountered.

        Returns:
            None
        """
        token = self.nextToken()
        if token.__class__ == IdentifierToken:
            # read the identifier token
            self.read(token)
            if token.value in ["true", "false", "nil", "dummy"]:
                # build the tree with the token value
                self.buildTree(token.value, 0)
            pass
        elif token.__class__ in [IntegerToken, StringToken]:
            # read the integer or string token
            self.read(token)
        elif token.__class__ == LParenToken:
            # read and ignore the ( token
            self.read(token, ignore=True)
        else:
            raise InvalidTokenException.fromToken(token)

    def parse(self):
            """Parses the source program and returns the Abstract Syntax Tree (AST).

            Returns:
                The Abstract Syntax Tree (AST) of the source program.
            """
            self.proc_R()
            return self.getAST()
    
