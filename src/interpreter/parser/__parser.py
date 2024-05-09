from interpreter.lexer import Lexer
from interpreter.lexer.tokens import *
from interpreter.ast import ASTNode

class Parser:
    """
    Parses the source code and builds the Abstract Syntax Tree (AST).
    
    Attributes:
        lexer (Lexer): The lexer object used for tokenizing the source code.
        nextToken (Token): The next token to be processed.
        stack (ParserStack): The stack used for parsing.
    """

    def __init__(self, src):
        """
        Initializes a Parser object.
        
        Args: 
            src (str): The source code to be parsed.
        
        """
        self.__lexer = Lexer(src)
        self.__nextToken:Token = self.__lexer.nextToken() 
        self.__stack = ParserStack()
        
    def __pushStack(self, token):
        self.__stack.push(token)
    
    def __popStack(self)->ASTNode:
        return self.__stack.pop()
    
    def nextToken(self)->Token:
        return self.__nextToken

    def lookahead(self)->Token:
        return self.__lexer.lookAhead()
    
    def __setNextToken(self, token):
        self.__nextToken = token
       
    def read(self, token, ignore=True):
        """
        Reads the next token in the parser and checks if it is the expected token. If not, raises an exception.
        Pushes the token to the stack as an ASTNode and gets the next token from the lexer.

        Args:
            token (str): The expected token.
            ignore (bool, optional): If True, the token will not be pushed to the stack. Defaults to True.

        Raises:
            Exception: If the next token is not the expected token.

        Returns:
            None
        """
        
        # helper function raise_invalid_token_exception
        #   :raise an exception with an error message
        def raise_invalid_token_exception(token, expected_token, line=None, col=None):
            err_msg = "Expected \"" + str(token) + "\" but found " + str(expected_token)
            if line is not None and col is not None:
                err_msg = err_msg + "\" at line " + str(line) + ", column " + str(col)
            raise InvalidTokenException(err_msg)
          
        # helper function to raise an exception based on the token type and value
        def raise_exception(token:Token, expected_token):

            _token_type = [LParenToken, RParenToken, SemiColonToken, CommaToken, KeywordToken]
            _operator_type = ["->", "&", "|", "@", ".", "=", "."]  
            
            _token = token
            _expected_token = expected_token
            _line = None
            _col = None
            
            if _token is not None:
                _line = _token.line
                _col = _token.col
            
            if token.isType(OperatorToken) and token.getValue() in _operator_type:
                _token = token.getValue()
            elif token.type not in _token_type:
                _token = token.getType()
                
            raise_invalid_token_exception(_token, _expected_token, _line, _col)
            
        # get the next token from the lexer
        _next_token = self.nextToken()
        
        # raise an exception if the next token is not the expected token
        if _next_token != token:
            raise_exception(token, _next_token)
        
        # push the token to the stack as an ASTNode and get the next token from the lexer
        if not ignore:
            self.__pushStack(ASTNode(self.nextToken()))
        self.__setNextToken(self.__getTokenFromLexer())
            

    def __getTokenFromLexer(self):
        """
        Retrieves the next token from the lexer.

        Returns:
            The next token from the lexer.
        """
        return self.__lexer.nextToken()
        
    def parse(self):
        """
        Parses the source code and returns the corresponding abstract syntax tree (AST).

        This method must be implemented by the subclass.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.

        Returns:
            AST: The abstract syntax tree representing the parsed source code.
        """
        # the lexer will be used to get tokens from the src as required
        raise NotImplementedError("parse method must be implemented by the subclass")
    
    def buildTree(self, x, n):
        """
        Builds a tree with the given root value and number of children.

        Args:
            x (str): The value of the root node.
            n (int): The number of children nodes.

        Returns:
            None
        """
        try: 
            p = None
            for i in range(n):
                c = self.__popStack()
                c.setRight(p) # set right sibling
                p = c
            self.__pushStack(ASTNode(x, p, None))
        except:
            raise BuildTreeException()
        
    def getAST(self)->ASTNode:
        return self.__popStack()
    
class ParserStack:
    """
    Represents the stack used to implement the parser.
    """
    def __init__(self):
        self.__stack:ASTNode = []
        
    def push(self, token:ASTNode):
        self.__stack.append(token)
        
    def pop(self)->ASTNode:
        if len(self.__stack) == 0:
            return None
        return self.__stack.pop()
    
    def top(self)->ASTNode:
        return self.__stack[-1]