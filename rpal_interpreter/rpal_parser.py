from .parser import Parser
from .tokens import *
class RPALParser(Parser):
    def __init__(self,src):
        super().__init__(src)
        
    def proc_At(self):
        """
        Process the At production rule.
        """
        self.proc_Af()
        self.__readSemiColon()
        
        _next_token = self.nextToken()
        while (_next_token.__class__ == OperatorToken 
            and (_next_token.isValue("*")) or _next_token.isValue("/")):
        
            # read the operator token and build the tree using the appropriate transduction rule
            if _next_token.isValue("*"):
                self.read(OperatorToken.fromValue("*"))
                self.proc_Af()
                self.buildTree("*", 2)
            else:
                self.read(OperatorToken.fromValue("/"))
                self.proc_Af()
                self.buildTree("/", 2)
            # update the next token
            _next_token = self.nextToken()

    def proc_Af(self):
        """
        Process the Af production rule.
        """
        self.proc_Ap()
        if self.nextToken().__class__ == SemiColonToken:
            self.__readSemiColon()
        elif self.nextToken().isValue("**"):
            self.read(OperatorToken.fromValue("**"), ignore=True)
            self.proc_Af()
            self.buildTree("**", 2)
        else:
            raise InvalidTokenException.fromToken(self.nextToken())
        
    def proc_Ap(self):
        """Parse the Ap production rule."""
        
        self.proc_R()
        self.__readSemiColon()
            
        # check if the next token is a @ 
        token = self.nextToken()
        while token != None and token.isValue("@"):
            # read the @ token and ignore it
            self.read(OperatorToken.fromValue("@"))
            
            # next token should be an identifier
            token = self.nextToken()
            self.read(IdentifierToken.fromValue(token.value))
            
            self.proc_R()
            self.buildTree("@", 3)

    def proc_R(self):
        """Parse the R production rule."""
        self.proc_Rn()
        self.__readSemiColon()
        n = 1
        while self.nextToken().__class__ in RPALParser.__FIRST_RN:
            self.proc_Rn()
            n += 1
        self.buildTree("gamma", n)
        
    __FIRST_RN = [IdentifierToken, IntegerToken, StringToken, LParenToken]
        
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
            self.read(token, ignore=False)
            if token.value in ["true", "false", "nil", "dummy"]:
                # build the tree with the token value
                self.buildTree(token.value, 0)
            pass
        elif token.__class__ in [IntegerToken, StringToken]:
            # read the integer or string token
            self.read(token, ignore = False)
        elif token.__class__ == LParenToken:
            # read and ignore the ( token
            self.read(token)
        else:
            raise InvalidTokenException.fromToken(token)

    def __readSemiColon(self):
        """Reads the semicolon token if it is present in the source program and ignores it."""
        self.read(SemiColonToken.instance())
            
    def parse(self):
            """Parses the source program and returns the Abstract Syntax Tree (AST).

            Returns:
                The Abstract Syntax Tree (AST) of the source program.
            """
            self.proc_Ap()
            return self.getAST()
    
