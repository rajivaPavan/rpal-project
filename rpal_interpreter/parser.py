from .lexer import Lexer

class Parser:
    def __init__(self, src):
        lexer = Lexer(src) 
        
    def parse(self):
        # the lexer will be used to get tokens from the src as required
        return "parsed ast"