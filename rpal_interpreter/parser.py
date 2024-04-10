from .lexer import Lexer
from .tokens import *
from .ast import ASTNode

class Parser:
    """
    The Parser class is responsible for parsing the source code and building the Abstract Syntax Tree (AST).
    """

    def __init__(self, src):
        """
        Initializes a Parser object.

        Parameters:
        - src (str): The source code to be parsed.

        Attributes:
        - __lexer (Lexer): The lexer object used for tokenizing the source code.
        - __nextToken (Token): The next token to be processed.
        - __stack (ParserStack): The stack used for parsing.

        Returns:
        - None
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

        Parameters:
            token (str): The expected token.
            ignore (bool, optional): If True, the token will not be pushed to the stack. Defaults to True.

        Raises:
            Exception: If the next token is not the expected token.

        Returns:
            None
        """
        
        _next_token = self.nextToken()
        if _next_token != token:
            
            """
            Prints custom ERROR messages for different types of tokens.
            
            token_type1: Tokens with exact values
            operator_type1: Tokens with exact values for OperatorToken
            
            """
            token_type1 = [LParenToken, RParenToken, SemiColonToken, CommaToken]
            operator_type1 = ["->", "&", "|", "@", ".", "=", "."]  
            
            # Raise error for none token
            if _next_token == None:
                raise InvalidTokenException("Expected token \"" + str(token) + "\" but found " + str(_next_token)+ ".")
            
            
            # Raise error for keyword token
            elif token.isType(KeywordToken):          
                raise InvalidTokenException("Expected token \"" + str(token) + "\" but found \"" + str(_next_token)
                    + "\" at line " + str(_next_token.line) + ", column " + str(_next_token.col) + " in the source code.")
                
            
            # Raise error for tokens with exact values 
            elif token.isType(token_type1):
                raise InvalidTokenException("Expected " + str(token) + " but found " + str(_next_token)
                    + " at line " + str(_next_token.line) + ", column " + str(_next_token.col) + " in the source code.")
                
                
            # Raise errors for other tokens
            else:
                
                #Print the required value of the token for the operator_type1 in the error message        
                if token.isType(OperatorToken) and token.getValue() in operator_type1:
                    raise InvalidTokenException("Expected \"" + token.getValue() + "\" but found " + str(_next_token)
                    + " at line " + str(_next_token.line) + ", column " + str(_next_token.col) + " in the source code.")
                    
                    
                else:     
                    raise InvalidTokenException("Expected " + token.getType() + " but found " + str(_next_token)
                        + " at line " + str(_next_token.line) + ", column " + str(_next_token.col) + " in the source code.")
                            
                            
        else:
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
                c.setRightSibling(p)
                p = c
            self.__pushStack(ASTNode(x, p, None))
        except:
            raise BuilTreeException("Error building the tree.")
        
    def getAST(self)->ASTNode:
        return self.__popStack()
    
class ParserStack:
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