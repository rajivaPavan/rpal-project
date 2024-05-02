from .lexer import *
from .rpal_parser import RPALParser
from .tokens import *

class Interpreter:
    def __init__(self):
        pass
    
    def interpret(self, program, ast_switch = False):
        """
        Interpret the given program
        
        args: 
            program - the source code
            ast_switch - whether to print the ast or the result
        """
        
        # Get the ast from the parser
        parser = RPALParser(program)
        try: 
            ast = parser.parse()
            
        except InvalidTokenException as e:
            print(e)
            return
        
        # Check if the program was fully parsed
        try:
            if parser.nextToken() != None:
                raise BuiltTreeException("Program not fully parsed. Has extra tokens.")
        except BuiltTreeException as e:
            self.result(ast, ast_switch)
            print(e)
            return
        except InvalidTokenException as e:
            print(e)
            return
            
        self.result(ast, ast_switch)

        return
    
        
    def result(self, ast, has_ast_switch):
        """Print the ast or the result"""
        if has_ast_switch:
            print(ast)
        else:
            output = Interpreter.__compute(ast)
            print(output)

    def __compute(ast):
        return "computed result"

