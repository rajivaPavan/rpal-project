from .lexer import Lexer
from .tokens import Token
from .ast import ASTNode

class Parser:
    def __init__(self, src):
        self.__lexer = Lexer(src)
        self.__nextToken:Token = self.__lexer.nextToken() 
        self.__stack = ParserStack()
        
    def __pushStack(self, token):
        self.__stack.push(token)
    
    def __popStack(self)->ASTNode:
        return self.__stack.pop()
    
    def nextToken(self)->Token:
        return self.__nextToken
    
    def __setNextToken(self, token):
        self.__nextToken = token
       
    def read(self, token):
        if self.nextToken() != token:
            raise Exception("Expected token: " + str(token) + " but found: " + str(self.nextToken()))    
        self.__pushStack(ASTNode(self.nextToken()))
        self.__setNextToken(self.__getTokenFromLexer())

    def __getTokenFromLexer(self):
        return self.__lexer.nextToken()
        
    def parse(self):
        # the lexer will be used to get tokens from the src as required
        raise NotImplementedError("parse method must be implemented by the subclass")
    
    def buildTree(self, x, n):     
        p = None
        for i in range(n):
            token = self.__popStack()
            c = ASTNode(token)
            c.setRightSibling(p)
            p = c
        self.__pushStack(ASTNode(x, p, None))
        
    def getAST(self)->ASTNode:
        return self.__popStack()

   
class ParserStack:
    def __init__(self):
        self.__stack:ASTNode = []
        
    def push(self, token:ASTNode):
        self.__stack.append(token)
        
    def pop(self)->ASTNode:
        return self.__stack.pop()